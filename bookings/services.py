"""
Bookings services - Concurrency-safe slot locking, pricing snapshots, and booking lifecycle.
"""
import random
import string
from datetime import datetime, timezone, timedelta
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from bookings.documents import Booking, SlotLock, PricingSnapshot
from core.services import log_audit_event

def generate_booking_reference():
    """
    Generates a unique 6-character alphanumeric reference prefixed with EVS-.
    e.g., EVS-K8N2P4
    """
    chars = string.ascii_uppercase + "23456789"  # exclude easily confused 0/O, 1/I
    suffix = "".join(random.choices(chars, k=6))
    return f"EVS-{suffix}"

def calculate_pricing(charger, duration_hours=1.0):
    """
    Computes transparent server-side pricing breakdown:
    - Estimated Energy (kWh): power_kw * hours * 0.85
    - Energy Subtotal: energy_kwh * price_per_kwh
    - Platform Commission: 15% of subtotal
    - GST: 18% on platform commission fee
    - Total Amount: subtotal + platform_fee + gst
    """
    hours = max(1.0, float(duration_hours))
    power = float(charger.power_output_kw)
    rate = float(charger.price_per_kwh)
    
    # Practical average acceptance factor on EV battery charging curve
    estimated_kwh = round(power * hours * 0.85, 1)
    subtotal = round(estimated_kwh * rate, 2)
    platform_fee = round(subtotal * 0.15, 2)
    gst = round(platform_fee * 0.18, 2)
    total = round(subtotal + platform_fee + gst, 2)
    
    return PricingSnapshot(
        rate_per_kwh=rate,
        estimated_energy_kwh=estimated_kwh,
        subtotal_amount=subtotal,
        platform_fee=platform_fee,
        gst_amount=gst,
        total_amount=total,
        currency='INR'
    )

def create_booking(driver, charger, slot_start_dt, slot_end_dt, vehicle=None):
    """
    Atomic reservation workflow:
    1. Validates charger bookability and non-self-booking rule.
    2. Atomically claims SlotLock using MongoDB compound unique index.
    3. Persists confirmed Booking document with immutable price snapshot.
    """
    if str(driver.id) == str(charger.host.id):
        raise ValueError("Hosts cannot book their own charger.")
        
    if not charger.is_bookable:
        raise ValueError("This charger is currently inactive or pending administrative approval.")
        
    now_utc = datetime.now(timezone.utc)
    if slot_start_dt <= now_utc:
        raise ValueError("Cannot book a time slot in the past.")
        
    if slot_start_dt >= slot_end_dt:
        raise ValueError("Invalid time range: slot start must precede slot end.")

    # Concurrency check & atomic slot reservation
    # Check if a lock already exists for this slot
    existing_lock = SlotLock.objects(charger=charger, slot_start=slot_start_dt).first()
    if existing_lock:
        raise ValueError("This slot has already been reserved by another driver. Please choose an alternate slot.")
        
    ref = generate_booking_reference()
    while Booking.objects(booking_reference=ref).first():
        ref = generate_booking_reference()

    # Create slot lock atomically
    try:
        lock = SlotLock(
            charger=charger,
            slot_start=slot_start_dt,
            slot_end=slot_end_dt,
            booking_ref=ref,
            locked_at=datetime.now(timezone.utc)
        )
        lock.save()
    except (DuplicateKeyError, Exception) as exc:
        raise ValueError("This slot was just claimed concurrently by another driver. Please pick another available slot.") from exc

    duration = max(1.0, (slot_end_dt - slot_start_dt).total_seconds() / 3600.0)
    pricing = calculate_pricing(charger, duration)
    
    booking = Booking(
        booking_reference=ref,
        driver=driver,
        host=charger.host,
        charger=charger,
        vehicle=vehicle,
        slot_start=slot_start_dt,
        slot_end=slot_end_dt,
        pricing_snapshot=pricing,
        status='confirmed',
        payment_status='unpaid',
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    booking.save()
    
    log_audit_event(
        actor_id=driver.id,
        actor_email=driver.email,
        action="booking_created",
        target_type="Booking",
        target_id=booking.id,
        details={
            "ref": ref,
            "charger": charger.title,
            "slot": slot_start_dt.isoformat(),
            "total": pricing.total_amount
        }
    )
    return booking

def cancel_booking(booking, actor_user, reason=""):
    """
    Cancels an eligible booking, safely releases the SlotLock, and updates refund state if paid.
    """
    actor_id = str(actor_user.id)
    is_driver = actor_id == str(booking.driver.id)
    is_host = actor_id == str(booking.host.id)
    is_admin = actor_user.is_superuser or 'admin' in actor_user.roles
    
    if not (is_driver or is_host or is_admin):
        raise PermissionError("You are not authorized to cancel this booking.")
        
    if not booking.is_cancellable:
        raise ValueError(f"Booking in status '{booking.status}' cannot be cancelled.")
        
    booking.status = 'cancelled'
    booking.cancelled_by = actor_user.email
    booking.cancellation_reason = (reason or "").strip()
    booking.cancelled_at = datetime.now(timezone.utc)
    booking.updated_at = datetime.now(timezone.utc)
    
    if booking.payment_status == 'simulated_paid':
        booking.payment_status = 'refunded'
        
    booking.save()
    
    # Release the slot lock to free up capacity
    SlotLock.objects(charger=booking.charger, slot_start=booking.slot_start).delete()
    
    log_audit_event(
        actor_id=actor_user.id,
        actor_email=actor_user.email,
        action="booking_cancelled",
        target_type="Booking",
        target_id=booking.id,
        details={"ref": booking.booking_reference, "reason": reason}
    )
    return booking
