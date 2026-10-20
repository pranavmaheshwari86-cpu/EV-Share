"""
Chargers views - Search explorer, charger detail, host management, and low-battery finder.
"""
import json
from datetime import datetime, timezone, date
from bson import ObjectId
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from chargers.documents import Charger, AvailabilityRule, BlackoutPeriod
from chargers.services import (
    search_chargers,
    create_charger,
    update_charger,
    toggle_charger_status,
    check_compatibility,
    get_available_slots_for_date
)
from accounts.decorators import login_required_mongo, role_required_mongo

def search_chargers_view(request):
    """
    Corridor & Map search view with interactive Leaflet map and filters.
    """
    query = request.GET.get('q', '').strip()
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    connector = request.GET.get('connector', '').strip()
    charger_type = request.GET.get('type', '').strip()
    min_power = request.GET.get('min_power', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    
    # Default to Greater Noida / Yamuna Expressway corridor coordinates if not specified
    # Greater Noida: 28.4744, 77.5040 | Mathura: 27.4924, 77.6737 | Agra: 27.1767, 78.0081
    corridor_center = {
        'lat': float(lat) if lat else 28.1000,
        'lng': float(lng) if lng else 77.7500,
    }
    
    results = search_chargers(
        lat=lat,
        lng=lng,
        connector=connector or None,
        charger_type=charger_type or None,
        min_power=min_power or None,
        max_price=max_price or None,
        query=query or None
    )
    
    # Prepare map markers data in GeoJSON-friendly JSON for Leaflet
    markers = []
    for r in results:
        c = r['charger']
        if c.latitude and c.longitude:
            markers.append({
                'id': str(c.id),
                'title': c.title,
                'lat': c.latitude,
                'lng': c.longitude,
                'power': c.power_output_kw,
                'type': c.charger_type,
                'connectors': c.connector_types,
                'price': c.price_per_kwh,
                'city': c.address.city,
                'url': f"/chargers/{c.id}/",
                'distance': f"{r['distance_km']} km" if r['distance_km'] is not None else None,
            })
            
    context = {
        'results': results,
        'results_count': len(results),
        'markers_json': json.dumps(markers),
        'corridor_center': corridor_center,
        'query': query,
        'selected_connector': connector,
        'selected_type': charger_type,
        'selected_min_power': min_power,
        'selected_max_price': max_price,
        'page_title': 'Discover EV Chargers — Yamuna Expressway Corridor',
    }
    return render(request, 'chargers/search.html', context)

def charger_detail_view(request, charger_id):
    """
    Charger specifications, pricing breakdown, vehicle compatibility check, and slot picker.
    """
    try:
        charger = Charger.objects(id=ObjectId(charger_id)).first()
    except Exception:
        raise Http404("Charger not found.")
        
    if not charger:
        raise Http404("Charger not found.")
        
    # Check compatibility if user is authenticated and has vehicles
    compatibility_info = None
    user = getattr(request, 'current_user', None)
    if user and user.vehicles:
        selected_vehicle = user.vehicles[0]
        is_compat, message = check_compatibility(charger, selected_vehicle)
        compatibility_info = {
            'vehicle': selected_vehicle,
            'is_compatible': is_compat,
            'message': message,
        }
        
    today_str = date.today().strftime("%Y-%m-%d")
    available_slots = get_available_slots_for_date(charger, today_str)
    
    context = {
        'charger': charger,
        'compatibility_info': compatibility_info,
        'available_slots': available_slots,
        'today_str': today_str,
        'page_title': f"{charger.title} — EV Share",
    }
    return render(request, 'chargers/detail.html', context)

def api_available_slots_view(request, charger_id):
    """
    AJAX endpoint: returns slots for a specified date (YYYY-MM-DD).
    """
    target_date = request.GET.get('date', date.today().strftime("%Y-%m-%d"))
    try:
        charger = Charger.objects(id=ObjectId(charger_id)).first()
        if not charger:
            return JsonResponse({'error': 'Charger not found'}, status=404)
            
        slots = get_available_slots_for_date(charger, target_date)
        return JsonResponse({'slots': slots, 'date': target_date})
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)

@login_required_mongo
@role_required_mongo('host')
def host_charger_list_view(request):
    """
    Host workspace: lists host's own chargers, verification badges, and control toggles.
    """
    user = request.current_user
    my_chargers = Charger.objects(host=user).order_by('-created_at')
    
    context = {
        'chargers': my_chargers,
        'page_title': 'My Charger Listings — Host Workspace',
    }
    return render(request, 'chargers/host_list.html', context)

@login_required_mongo
@role_required_mongo('host')
def create_charger_view(request):
    """
    Create a new charger listing. Requires verified host status or warning display.
    """
    user = request.current_user
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        charger_type = request.POST.get('charger_type', 'AC')
        connector_types = request.POST.getlist('connector_types')
        power_kw = request.POST.get('power_output_kw', 7.4)
        price_per_kwh = request.POST.get('price_per_kwh', 14.0)
        city = request.POST.get('city', 'Greater Noida').strip()
        display_address = request.POST.get('display_address', '').strip()
        private_directions = request.POST.get('private_directions', '').strip()
        lat = request.POST.get('latitude', 28.4744)
        lng = request.POST.get('longitude', 77.5040)
        amenities = request.POST.getlist('amenities')
        
        if not title or not description or not display_address or not connector_types:
            messages.error(request, "Please fill in all required fields including connector types and location.")
        else:
            try:
                charger = create_charger(
                    host=user,
                    title=title,
                    description=description,
                    charger_type=charger_type,
                    connector_types=connector_types,
                    power_kw=power_kw,
                    price_per_kwh=price_per_kwh,
                    city=city,
                    display_address=display_address,
                    private_directions=private_directions,
                    lat=lat,
                    lng=lng,
                    amenities=amenities
                )
                messages.success(request, f"Charger listing '{charger.title}' created and submitted for verification!")
                return redirect('chargers:host_list')
            except Exception as exc:
                messages.error(request, f"Error saving listing: {exc}")
                
    context = {
        'page_title': 'List Your Charger — EV Share Host',
    }
    return render(request, 'chargers/create.html', context)

@login_required_mongo
@role_required_mongo('host')
def edit_charger_view(request, charger_id):
    """
    Edit existing charger listing (verifying host ownership).
    """
    user = request.current_user
    try:
        charger = Charger.objects(id=ObjectId(charger_id), host=user).first()
    except Exception:
        raise Http404("Charger not found or access denied.")
        
    if not charger:
        messages.error(request, "You do not have permission to edit this listing.")
        return redirect('chargers:host_list')
        
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        charger_type = request.POST.get('charger_type', charger.charger_type)
        connector_types = request.POST.getlist('connector_types') or charger.connector_types
        power_kw = request.POST.get('power_output_kw', charger.power_output_kw)
        price_per_kwh = request.POST.get('price_per_kwh', charger.price_per_kwh)
        display_address = request.POST.get('display_address', charger.address.display_address)
        private_directions = request.POST.get('private_directions', charger.address.private_directions)
        amenities = request.POST.getlist('amenities')
        
        update_charger(
            charger,
            title=title,
            description=description,
            charger_type=charger_type,
            connector_types=connector_types,
            power_output_kw=float(power_kw),
            price_per_kwh=float(price_per_kwh),
            display_address=display_address,
            private_directions=private_directions,
            amenities=amenities
        )
        messages.success(request, "Listing updated successfully.")
        return redirect('chargers:host_list')
        
    context = {
        'charger': charger,
        'page_title': f"Edit {charger.title} — EV Share",
    }
    return render(request, 'chargers/edit.html', context)

@login_required_mongo
@role_required_mongo('host')
def toggle_charger_status_view(request, charger_id):
    """
    Toggles charger active / paused state.
    """
    user = request.current_user
    try:
        charger = Charger.objects(id=ObjectId(charger_id), host=user).first()
        if not charger:
            messages.error(request, "Listing not found or access denied.")
            return redirect('chargers:host_list')
            
        new_state = toggle_charger_status(charger)
        status_word = "Activated" if new_state else "Paused"
        messages.info(request, f"Listing '{charger.title}' is now {status_word}.")
    except Exception as exc:
        messages.error(request, f"Error toggling status: {exc}")
        
    return redirect('chargers:host_list')

def low_battery_view(request):
    """
    Low-Battery Assistance Mode:
    Rapid one-touch discovery prioritizing verified chargers with available slots nearest to user.
    """
    lat = request.GET.get('lat', '28.3500')
    lng = request.GET.get('lng', '77.5500')
    
    results = search_chargers(
        lat=lat,
        lng=lng,
        max_distance_km=60
    )
    
    context = {
        'results': results[:5],  # top 5 closest options
        'lat': lat,
        'lng': lng,
        'page_title': 'Urgent Low-Battery Assistance — Nearest Bookable Chargers',
    }
    return render(request, 'chargers/low_battery.html', context)
