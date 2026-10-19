"""
Bookings views - Checkout, confirmation, driver history, host reservations, and cancellation.
"""
from datetime import datetime, timezone
from bson import ObjectId
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from chargers.documents import Charger
from bookings.documents import Booking
from bookings.services import (
    create_booking,
    cancel_booking,
    calculate_pricing
)
from accounts.decorators import login_required_mongo, role_required_mongo

@login_required_mongo
def create_booking_view(request, charger_id):
    """
    Checkout view: driver confirms slot, reviews price breakdown, chooses vehicle, and books.
    """
    user = request.current_user
    try:
        charger = Charger.objects(id=ObjectId(charger_id)).first()
    except Exception:
        raise Http404("Charger not found.")
        
    if not charger or not charger.is_bookable:
        messages.error(request, "This charger is not currently eligible for booking.")
        return redirect('chargers:search')
        
    if str(user.id) == str(charger.host.id):
        messages.warning(request, "You cannot book your own charger listing.")
        return redirect('chargers:detail', charger_id=str(charger.id))

    slot_start_raw = request.GET.get('slot_start') or request.POST.get('slot_start')
    slot_end_raw = request.GET.get('slot_end') or request.POST.get('slot_end')
    
    if not slot_start_raw or not slot_end_raw:
        messages.warning(request, "Please select an available time slot on the charger page.")
        return redirect('chargers:detail', charger_id=str(charger.id))
        
    try:
        slot_start_dt = datetime.fromisoformat(slot_start_raw.replace('Z', '+00:00'))
        slot_end_dt = datetime.fromisoformat(slot_end_raw.replace('Z', '+00:00'))
    except Exception as exc:
        messages.error(request, f"Invalid time slot format: {exc}")
        return redirect('chargers:detail', charger_id=str(charger.id))
        
    duration = max(1.0, (slot_end_dt - slot_start_dt).total_seconds() / 3600.0)
    pricing = calculate_pricing(charger, duration)
    
    if request.method == 'POST':
        # Select vehicle if available
        vehicle = None
        veh_idx = request.POST.get('vehicle_index')
        if veh_idx and user.vehicles:
            try:
                vehicle = user.vehicles[int(veh_idx)]
            except (IndexError, ValueError):
                pass

        try:
            booking = create_booking(
                driver=user,
                charger=charger,
                slot_start_dt=slot_start_dt,
                slot_end_dt=slot_end_dt,
                vehicle=vehicle
            )
            messages.success(request, f"Booking {booking.booking_reference} confirmed!")
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
        except ValueError as err:
            messages.error(request, str(err))
            return redirect('chargers:detail', charger_id=str(charger.id))
            
    context = {
        'charger': charger,
        'slot_start_dt': slot_start_dt,
        'slot_end_dt': slot_end_dt,
        'pricing': pricing,
        'duration_hours': duration,
        'user_vehicles': user.vehicles,
        'page_title': f"Book {charger.title} — EV Share",
    }
    return render(request, 'bookings/checkout.html', context)

@login_required_mongo
def booking_detail_view(request, booking_ref):
    """
    Booking confirmation & detail page with authorized host directions, status, and actions.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    is_driver = str(user.id) == str(booking.driver.id)
    is_host = str(user.id) == str(booking.host.id)
    is_admin = user.is_superuser or 'admin' in user.roles
    
    if not (is_driver or is_host or is_admin):
        messages.error(request, "You are not authorized to view this booking record.")
        return redirect('home')

    # Fetch associated session if exists
    from sessions_app.documents import ChargingSession
    session_record = ChargingSession.objects(booking=booking).first()

    context = {
        'booking': booking,
        'is_driver': is_driver,
        'is_host': is_host,
        'is_admin': is_admin,
        'session_record': session_record,
        'page_title': f"Booking {booking.booking_reference} — EV Share",
    }
    return render(request, 'bookings/detail.html', context)

@login_required_mongo
def driver_booking_history_view(request):
    """
    Driver dashboard: list of all bookings created by the driver.
    """
    user = request.current_user
    bookings = Booking.objects(driver=user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'page_title': 'My Bookings — Driver Dashboard',
    }
    return render(request, 'bookings/driver_history.html', context)

@login_required_mongo
@role_required_mongo('host')
def host_reservations_view(request):
    """
    Host dashboard: list of reservations for the host's chargers.
    """
    user = request.current_user
    reservations = Booking.objects(host=user).order_by('-slot_start')
    
    context = {
        'reservations': reservations,
        'page_title': 'Incoming Reservations — Host Dashboard',
    }
    return render(request, 'bookings/host_reservations.html', context)

@login_required_mongo
def cancel_booking_view(request, booking_ref):
    """
    Cancellation view with policy warning and reason input.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        try:
            cancel_booking(booking, user, reason=reason)
            messages.info(request, f"Booking {booking.booking_reference} has been cancelled and the slot released.")
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
        except (ValueError, PermissionError) as err:
            messages.error(request, str(err))
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
            
    context = {
        'booking': booking,
        'page_title': f"Cancel Booking {booking.booking_reference} — EV Share",
    }
    return render(request, 'bookings/cancel.html', context)
