"""
Chargers services - Geospatial search, availability calculation, and CRUD operations.
"""
import math
from datetime import datetime, timezone, timedelta, time
from bson import ObjectId
from chargers.documents import Charger, ChargerAddress, AvailabilityRule, BlackoutPeriod
from core.services import log_audit_event

def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Computes great-circle distance between two coordinates in kilometers.
    """
    R = 6371.0  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def create_charger(host, title, description, charger_type, connector_types,
                   power_kw, price_per_kwh, city, display_address,
                   private_directions="", lat=28.4744, lng=77.5040, amenities=None, photos=None,
                   availability_rules=None):
    """
    Creates a new Charger document for review.
    """
    address = ChargerAddress(
        city=city.strip(),
        display_address=display_address.strip(),
        private_directions=private_directions.strip() if private_directions else ""
    )
    
    # GeoJSON coordinate ordering is [longitude, latitude]
    location = [float(lng), float(lat)]
    
    charger = Charger(
        host=host,
        title=title.strip(),
        description=description.strip(),
        charger_type=charger_type.strip(),
        connector_types=connector_types or ['Type 2'],
        power_output_kw=float(power_kw),
        price_per_kwh=float(price_per_kwh),
        address=address,
        location=location,
        amenities=amenities or [],
        photos=photos or [],
        verification_status='pending',
        is_active=True
    )
    
    # Setup default 8am - 8pm daily availability if not provided
    if not availability_rules:
        for day in range(7):
            charger.availability_rules.append(
                AvailabilityRule(day_of_week=day, start_time="08:00", end_time="20:00")
            )
    else:
        charger.availability_rules = availability_rules

    charger.save()
    
    log_audit_event(
        actor_id=host.id,
        actor_email=host.email,
        action="charger_created",
        target_type="Charger",
        target_id=charger.id,
        details={"title": charger.title, "power": charger.power_output_kw}
    )
    return charger

def update_charger(charger, **kwargs):
    """
    Updates mutable fields of a charger.
    """
    allowed_fields = [
        'title', 'description', 'charger_type', 'connector_types',
        'power_output_kw', 'price_per_kwh', 'amenities', 'photos', 'is_active'
    ]
    for key, value in kwargs.items():
        if key in allowed_fields and value is not None:
            setattr(charger, key, value)
            
    if 'display_address' in kwargs or 'private_directions' in kwargs:
        if 'display_address' in kwargs and kwargs['display_address']:
            charger.address.display_address = kwargs['display_address']
        if 'private_directions' in kwargs:
            charger.address.private_directions = kwargs['private_directions']
            
    charger.updated_at = datetime.now(timezone.utc)
    charger.save()
    return charger

def toggle_charger_status(charger):
    """
    Toggles is_active on the charger.
    """
    charger.is_active = not charger.is_active
    charger.updated_at = datetime.now(timezone.utc)
    charger.save()
    return charger.is_active

def search_chargers(lat=None, lng=None, max_distance_km=100, connector=None,
                    charger_type=None, min_power=None, max_price=None, query=None):
    """
    Search active and approved chargers with optional filters and proximity sorting.
    """
    q_filters = {
        'verification_status': 'approved',
        'is_active': True,
    }
    
    if charger_type:
        q_filters['charger_type'] = charger_type
        
    if connector:
        q_filters['connector_types'] = connector
        
    if min_power:
        try:
            q_filters['power_output_kw__gte'] = float(min_power)
        except (ValueError, TypeError):
            pass
            
    if max_price:
        try:
            q_filters['price_per_kwh__lte'] = float(max_price)
        except (ValueError, TypeError):
            pass

    chargers = list(Charger.objects(**q_filters))
    
    # Filter by text query if provided
    if query:
        q_lower = query.strip().lower()
        chargers = [
            c for c in chargers if (
                q_lower in c.title.lower() or
                q_lower in c.description.lower() or
                q_lower in c.address.city.lower() or
                q_lower in c.address.display_address.lower()
            )
        ]
        
    # Proximity calculation and sorting if coordinates provided
    results = []
    has_coords = lat is not None and lng is not None
    try:
        user_lat = float(lat) if lat is not None else None
        user_lng = float(lng) if lng is not None else None
    except (ValueError, TypeError):
        has_coords = False
        user_lat, user_lng = None, None

    for c in chargers:
        dist_km = None
        if has_coords and c.latitude is not None and c.longitude is not None:
            dist_km = round(haversine_distance_km(user_lat, user_lng, c.latitude, c.longitude), 1)
            if max_distance_km and dist_km > float(max_distance_km):
                continue
        results.append({
            'charger': c,
            'distance_km': dist_km
        })
        
    if has_coords:
        results.sort(key=lambda x: x['distance_km'] if x['distance_km'] is not None else 999999)
        
    return results

def check_compatibility(charger, vehicle):
    """
    Validates compatibility between vehicle and charger.
    Returns (is_compatible: bool, details: str).
    """
    if not vehicle:
        return True, "No vehicle specified. Inspect connector specs carefully."
        
    v_connector = vehicle.connector_type
    if v_connector in charger.connector_types:
        return True, f"Direct compatibility: vehicle connector {v_connector} matches charger."
        
    # Standard Indian compatibility rules:
    # CCS2 vehicles also support Type 2 AC chargers
    if v_connector == 'CCS2' and 'Type 2' in charger.connector_types:
        return True, "Compatible via Type 2 AC charging inlet on CCS2 port."
        
    # Type 2 vehicle attempting CCS2 DC
    if v_connector == 'Type 2' and 'CCS2' in charger.connector_types and 'Type 2' not in charger.connector_types:
        return False, "Incompatible: AC vehicle cannot plug into dedicated DC CCS2 plug."
        
    return False, f"Incompatible: Vehicle uses {v_connector}, but charger offers {', '.join(charger.connector_types)}."

def get_available_slots_for_date(charger, target_date):
    """
    Returns discrete 1-hour slots for a given date (YYYY-MM-DD),
    marking each as available or unavailable based on weekly rules, blackouts, and existing locks.
    """
    from bookings.documents import SlotLock
    
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        
    date_str = target_date.strftime("%Y-%m-%d")
    weekday = target_date.weekday()  # 0=Monday, 6=Sunday
    
    # Check blackouts
    for bo in charger.blackout_periods:
        if bo.date == date_str:
            return []  # Entire day is blocked
            
    # Check recurring weekly availability rules
    matching_rules = [r for r in charger.availability_rules if r.day_of_week == weekday]
    if not matching_rules:
        return []
        
    # Fetch existing SlotLocks for this charger on this date
    start_of_day = datetime(target_date.year, target_date.month, target_date.day, 0, 0, tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)
    
    existing_locks = set(
        lock.slot_start for lock in SlotLock.objects(
            charger=charger,
            slot_start__gte=start_of_day,
            slot_start__lt=end_of_day
        )
    )
    
    now_utc = datetime.now(timezone.utc)
    available_slots = []
    
    for rule in matching_rules:
        try:
            start_h, start_m = map(int, rule.start_time.split(':'))
            end_h, end_m = map(int, rule.end_time.split(':'))
        except Exception:
            continue
            
        current_dt = datetime(target_date.year, target_date.month, target_date.day, start_h, start_m, tzinfo=timezone.utc)
        rule_end_dt = datetime(target_date.year, target_date.month, target_date.day, end_h, end_m, tzinfo=timezone.utc)
        
        while current_dt + timedelta(hours=1) <= rule_end_dt:
            slot_start = current_dt
            slot_end = current_dt + timedelta(hours=1)
            
            # A slot in the past cannot be booked
            is_past = slot_start <= now_utc
            is_locked = slot_start in existing_locks
            
            available_slots.append({
                'slot_start': slot_start.isoformat(),
                'slot_end': slot_end.isoformat(),
                'start_time_str': slot_start.strftime("%H:%M"),
                'end_time_str': slot_end.strftime("%H:%M"),
                'display': f"{slot_start.strftime('%I:%M %p')} – {slot_end.strftime('%I:%M %p')}",
                'is_available': not is_past and not is_locked,
                'is_past': is_past,
                'is_locked': is_locked,
            })
            current_dt += timedelta(hours=1)
            
    return available_slots
