"""
Test suite for Security, Address Privacy Protection, and Role Boundaries.
"""
import pytest
from datetime import datetime, timezone, timedelta
from django.test import Client
from accounts.services import register_user
from chargers.services import create_charger
from bookings.services import create_booking

from accounts.documents import User
from chargers.documents import Charger
from bookings.documents import Booking, SlotLock

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
def sec_setup():
    admin = register_user(
        email="admin.sec@evshare.in",
        password="AdminPassword123!",
        full_name="Sec Admin",
        role="admin"
    )
    admin.is_superuser = True
    admin.save()

    host = register_user(
        email="host.sec@evshare.in",
        password="HostPassword123!",
        full_name="Sec Host",
        role="host"
    )

    driver_a = register_user(
        email="driver.a@evshare.in",
        password="DriverPassword123!",
        full_name="Driver Alpha",
        role="driver"
    )

    driver_b = register_user(
        email="driver.b@evshare.in",
        password="DriverPassword123!",
        full_name="Driver Bravo",
        role="driver"
    )

    charger = create_charger(
        host=host,
        title="Privacy Test Charger",
        description="Testing directions privacy",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=50.0,
        price_per_kwh=16.0,
        city="Greater Noida",
        display_address="Near Pari Chowk (Public)",
        private_directions="Confidential: Gate Code 9988 behind security office",
        lat=28.4744,
        lng=77.5040
    )
    charger.verification_status = "approved"
    charger.is_active = True
    charger.save()

    return admin, host, driver_a, driver_b, charger

def test_unauthenticated_redirect_to_login():
    """Verify protected routes redirect unauthenticated visitors to login."""
    client = Client()
    
    # Try accessing host dashboard without auth
    resp1 = client.get('/chargers/mine/')
    assert resp1.status_code == 302
    assert '/accounts/login/' in resp1.url
    
    # Try accessing driver history without auth
    resp2 = client.get('/bookings/history/')
    assert resp2.status_code == 302
    assert '/accounts/login/' in resp2.url

    # Try accessing admin portal without auth
    resp3 = client.get('/administration/')
    assert resp3.status_code == 302
    assert '/accounts/login/' in resp3.url

def test_role_boundary_driver_cannot_access_admin(sec_setup):
    """Verify regular driver cannot access admin portal."""
    admin, host, driver_a, driver_b, charger = sec_setup
    
    client = Client()
    # Log in as Driver A
    client.post('/accounts/login/', {
        'email': 'driver.a@evshare.in',
        'password': 'DriverPassword123!'
    })
    
    # Attempt admin dashboard
    resp = client.get('/administration/')
    # Should redirect with permission error
    assert resp.status_code == 302
    assert resp.url != '/administration/'

def test_address_privacy_on_public_screens(sec_setup):
    """Verify public charger details do NOT expose confidential private driveway directions."""
    admin, host, driver_a, driver_b, charger = sec_setup
    client = Client()
    
    # Public view of charger details
    resp = client.get(f'/chargers/{charger.id}/')
    assert resp.status_code == 200
    
    content = resp.content.decode('utf-8')
    # Public display address should be visible
    assert "Near Pari Chowk (Public)" in content
    # Confidential private directions MUST NOT be visible on public detail page
    assert "Confidential: Gate Code 9988" not in content

def test_cross_user_booking_isolation(sec_setup):
    """Verify Driver B cannot access private instructions of Driver A's booking."""
    admin, host, driver_a, driver_b, charger = sec_setup
    
    slot_start = datetime.now(timezone.utc) + timedelta(days=1)
    slot_end = slot_start + timedelta(hours=1)
    booking_a = create_booking(
        driver=driver_a,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )

    client_b = Client()
    client_b.post('/accounts/login/', {
        'email': 'driver.b@evshare.in',
        'password': 'DriverPassword123!'
    })

    # Driver B tries to access Driver A's booking pass
    resp = client_b.get(f'/bookings/{booking_a.booking_reference}/')
    # Should be denied access and redirected
    assert resp.status_code == 302
