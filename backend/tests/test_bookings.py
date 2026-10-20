"""
Test suite for Booking concurrency, atomic slot locking, pricing snapshots, and cancellations.
"""
import pytest
from datetime import datetime, timezone, timedelta
from accounts.documents import User, Vehicle
from accounts.services import register_user
from chargers.documents import Charger, ChargerAddress
from chargers.services import create_charger
from bookings.documents import Booking, SlotLock
from bookings.services import (
    create_booking,
    cancel_booking,
    calculate_pricing
)

@pytest.fixture(autouse=True)
def clean_db():
    SlotLock.objects.delete()
    Booking.objects.delete()
    Charger.objects.delete()
    User.objects.delete()
    yield
    SlotLock.objects.delete()
    Booking.objects.delete()
    Charger.objects.delete()
    User.objects.delete()

@pytest.fixture
def booking_setup():
    host = register_user(
        email="host.bk@evshare.in",
        password="Password123!",
        full_name="Booking Host",
        role="host"
    )
    driver1 = register_user(
        email="driver1@evshare.in",
        password="Password123!",
        full_name="Driver One",
        role="driver"
    )
    driver2 = register_user(
        email="driver2@evshare.in",
        password="Password123!",
        full_name="Driver Two",
        role="driver"
    )
    charger = create_charger(
        host=host,
        title="Yamuna KM 50 Hub",
        description="Fast charger",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=50.0,
        price_per_kwh=16.0,
        city="Jewar",
        display_address="KM 50",
        private_directions="Secret Gate Code 1234",
        lat=28.0000,
        lng=77.5500
    )
    charger.verification_status = "approved"
    charger.is_active = True
    charger.save()

    return host, driver1, driver2, charger

def test_atomic_booking_creation_and_lock(booking_setup):
    """Verify booking succeeds and atomic slot lock is created."""
    host, driver1, driver2, charger = booking_setup
    
    slot_start = datetime.now(timezone.utc) + timedelta(days=1)
    slot_end = slot_start + timedelta(hours=1)
    
    booking = create_booking(
        driver=driver1,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )
    assert booking is not None
    assert booking.status == "confirmed"
    assert booking.booking_reference.startswith("EVS-")
    
    # Verify slot lock exists
    lock = SlotLock.objects(charger=charger, slot_start=slot_start).first()
    assert lock is not None
    assert lock.booking_ref == booking.booking_reference

def test_concurrency_double_booking_rejection(booking_setup):
    """Verify that a second booking attempt on the same slot is rejected atomically."""
    host, driver1, driver2, charger = booking_setup
    
    slot_start = datetime.now(timezone.utc) + timedelta(days=2)
    slot_end = slot_start + timedelta(hours=1)
    
    # Driver 1 claims slot
    b1 = create_booking(
        driver=driver1,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )
    assert b1 is not None

    # Driver 2 attempts to claim the identical slot
    with pytest.raises(ValueError, match="already been reserved"):
        create_booking(
            driver=driver2,
            charger=charger,
            slot_start_dt=slot_start,
            slot_end_dt=slot_end
        )

def test_host_cannot_book_own_charger(booking_setup):
    """Verify host cannot create a booking on their own charger."""
    host, driver1, driver2, charger = booking_setup
    
    slot_start = datetime.now(timezone.utc) + timedelta(days=3)
    slot_end = slot_start + timedelta(hours=1)
    
    with pytest.raises(ValueError, match="cannot book their own charger"):
        create_booking(
            driver=host,
            charger=charger,
            slot_start_dt=slot_start,
            slot_end_dt=slot_end
        )

def test_booking_cancellation_releases_slot(booking_setup):
    """Verify cancellation marks booking cancelled, releases slot lock, and allows re-booking."""
    host, driver1, driver2, charger = booking_setup
    
    slot_start = datetime.now(timezone.utc) + timedelta(days=4)
    slot_end = slot_start + timedelta(hours=1)
    
    # Driver 1 books
    b1 = create_booking(
        driver=driver1,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )
    assert SlotLock.objects(charger=charger, slot_start=slot_start).count() == 1

    # Driver 1 cancels
    cancel_booking(b1, driver1, reason="Change of plans")
    b1.reload()
    assert b1.status == "cancelled"
    
    # Slot lock should be deleted
    assert SlotLock.objects(charger=charger, slot_start=slot_start).count() == 0

    # Now Driver 2 can book the newly released slot without error
    b2 = create_booking(
        driver=driver2,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )
    assert b2.status == "confirmed"
    assert b2.driver == driver2
