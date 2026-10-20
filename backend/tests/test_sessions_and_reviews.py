"""
Test suite for Charging Sessions, Meter delta telemetry, Driver Reviews, and Support Tickets.
"""
import pytest
from datetime import datetime, timezone, timedelta
from django.test import Client
from accounts.documents import User
from accounts.services import register_user
from chargers.documents import Charger
from chargers.services import create_charger
from bookings.documents import Booking, SlotLock
from bookings.services import create_booking
from sessions_app.documents import ChargingSession
from sessions_app.services import start_charging_session, end_charging_session, report_session_issue
from reviews.documents import Review
from reviews.services import submit_review
from support.documents import SupportCase
from support.services import create_support_ticket, resolve_support_ticket

@pytest.fixture(autouse=True)
def clean_db():
    Review.objects.delete()
    SupportCase.objects.delete()
    ChargingSession.objects.delete()
    SlotLock.objects.delete()
    Booking.objects.delete()
    Charger.objects.delete()
    User.objects.delete()
    yield
    Review.objects.delete()
    SupportCase.objects.delete()
    ChargingSession.objects.delete()
    SlotLock.objects.delete()
    Booking.objects.delete()
    Charger.objects.delete()
    User.objects.delete()

@pytest.fixture
def session_fixture():
    host = register_user(
        email="host.session@evshare.in",
        password="Password123!",
        full_name="Host Session",
        role="host"
    )
    driver = register_user(
        email="driver.session@evshare.in",
        password="Password123!",
        full_name="Driver Session",
        role="driver"
    )
    charger = create_charger(
        host=host,
        title="Noida Sector 128 Fast Charger",
        description="High speed charger",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=60.0,
        price_per_kwh=18.0,
        city="Greater Noida",
        display_address="Expressway Hub KM 15",
        private_directions="Tower B Basement 2",
        lat=28.4744,
        lng=77.5040
    )
    charger.verification_status = "approved"
    charger.is_active = True
    charger.save()

    now = datetime.now(timezone.utc)
    slot_start = (now + timedelta(hours=2)).replace(minute=0, second=0, microsecond=0)
    slot_end = slot_start + timedelta(hours=1)

    booking = create_booking(
        driver=driver,
        charger=charger,
        slot_start_dt=slot_start,
        slot_end_dt=slot_end
    )
    booking.status = "confirmed"
    booking.save()

    return {
        "host": host,
        "driver": driver,
        "charger": charger,
        "booking": booking
    }

def test_charging_session_lifecycle(session_fixture):
    booking = session_fixture["booking"]
    driver = session_fixture["driver"]

    # 1. Start charging visit
    session = start_charging_session(
        booking=booking,
        actor_user=driver,
        meter_start=150.0,
        notes="Plugged in CCS2 securely"
    )
    assert session.session_status == "started"
    assert session.meter_start_kwh == 150.0
    booking.reload()
    assert booking.status == "in_progress"

    # 2. End charging visit with meter reading
    completed_session = end_charging_session(
        session=session,
        actor_user=driver,
        meter_end=178.5,
        notes="Battery charged to 80%"
    )
    assert completed_session.session_status == "completed"
    assert completed_session.meter_end_kwh == 178.5
    assert completed_session.actual_energy_kwh == 28.5
    booking.reload()
    assert booking.status == "completed"

def test_review_submission_and_rating_recalc(session_fixture):
    booking = session_fixture["booking"]
    driver = session_fixture["driver"]
    host = session_fixture["host"]
    charger = session_fixture["charger"]

    # Mark booking completed
    booking.status = "completed"
    booking.save()

    # Driver submits 5-star review
    review = submit_review(
        booking=booking,
        driver=driver,
        rating=5,
        comment="Flawless charging experience on the Yamuna Expressway!"
    )
    assert review.rating == 5
    charger.reload()
    assert charger.average_rating == 5.0
    assert charger.reviews_count == 1

    # Duplicate review should fail
    with pytest.raises(ValueError, match="already been submitted"):
        submit_review(booking=booking, driver=driver, rating=4, comment="Another review")

    # Host cannot submit review for their own charger
    with pytest.raises(PermissionError):
        submit_review(booking=booking, driver=host, rating=5, comment="I am the host")

def test_support_ticket_flow(session_fixture):
    driver = session_fixture["driver"]
    booking = session_fixture["booking"]

    ticket = create_support_ticket(
        user=driver,
        subject="Dispute regarding parking gate code",
        category="session_problem",
        description="Host gate phone was not reachable for 10 minutes",
        related_booking=booking
    )
    assert ticket.ticket_id.startswith("CASE-")
    assert ticket.status == "open"

    admin_user = session_fixture["host"]  # Host acts as admin here
    admin_user.roles.append("admin")
    admin_user.save()

    resolved = resolve_support_ticket(
        ticket=ticket,
        admin_user=admin_user,
        resolution_notes="Contacted host and updated entry instructions."
    )
    assert resolved.status == "resolved"
    assert resolved.resolution_notes != ""

def test_health_check_endpoint():
    client = Client()
    response = client.get('/health/')
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["platform"] == "EV Share"
    assert "database" in data
