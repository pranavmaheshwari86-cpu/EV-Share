"""
Sessions views - Interface for starting/ending visits and reporting issues.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from bookings.documents import Booking
from sessions_app.documents import ChargingSession
from sessions_app.services import (
    start_charging_session,
    end_charging_session,
    report_session_issue
)
from accounts.decorators import login_required_mongo

@login_required_mongo
def start_session_view(request, booking_ref):
    """
    Host or driver checks in and starts the physical charging session.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    if request.method == 'POST':
        meter_start = request.POST.get('meter_start_kwh', 0.0)
        notes = request.POST.get('notes', '')
        try:
            start_charging_session(booking, user, meter_start=meter_start, notes=notes)
            messages.success(request, f"Charging session for {booking.booking_reference} started!")
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
        except (PermissionError, ValueError) as err:
            messages.error(request, str(err))
            
    context = {
        'booking': booking,
        'page_title': f"Start Charging Visit — {booking.booking_reference}",
    }
    return render(request, 'sessions/start_session.html', context)

@login_required_mongo
def end_session_view(request, booking_ref):
    """
    Host or driver records visit completion and meter reading.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    session = ChargingSession.objects(booking=booking).first()
    if not session:
        messages.error(request, "Charging session has not been initiated yet.")
        return redirect('bookings:detail', booking_ref=booking.booking_reference)
        
    if request.method == 'POST':
        meter_end = request.POST.get('meter_end_kwh', 0.0)
        notes = request.POST.get('notes', '')
        try:
            end_charging_session(session, user, meter_end=meter_end, notes=notes)
            messages.success(request, f"Charging session completed! Thank you for sharing.")
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
        except (PermissionError, ValueError) as err:
            messages.error(request, str(err))
            
    context = {
        'booking': booking,
        'session': session,
        'page_title': f"Complete Charging Visit — {booking.booking_reference}",
    }
    return render(request, 'sessions/end_session.html', context)

@login_required_mongo
def report_issue_view(request, booking_ref):
    """
    Report an issue or dispute during a charging visit.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    session = ChargingSession.objects(booking=booking).first()
    if not session:
        # Create initial session if none exists so dispute can attach
        session = ChargingSession(
            booking=booking,
            charger=booking.charger,
            driver=booking.driver,
            host=booking.host,
            session_status='disputed'
        )
        session.save()
        
    if request.method == 'POST':
        issue_text = request.POST.get('issue_description', '').strip()
        if not issue_text:
            messages.error(request, "Please describe the problem encountered.")
        else:
            report_session_issue(session, user, issue_text)
            messages.warning(request, "Problem reported. A support case has been opened and flagged for administrator review.")
            return redirect('bookings:detail', booking_ref=booking.booking_reference)
            
    context = {
        'booking': booking,
        'session': session,
        'page_title': f"Report Problem — Booking {booking.booking_reference}",
    }
    return render(request, 'sessions/report_issue.html', context)
