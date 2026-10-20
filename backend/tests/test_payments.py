"""
Test suite for Simulated Payment sandbox, transaction states, and financial ledger calculations.
"""
import pytest
from datetime import datetime, timezone, timedelta
from accounts.services import register_user
from chargers.services import create_charger
from bookings.services import create_booking
from payments.documents import PaymentTransaction
from payments.services import (
    create_or_get_transaction,
    process_simulated_payment,
    refund_simulated_payment
)

from bookings.documents import Booking, SlotLock
from chargers.documents import Charger
from accounts.documents import User

@pytest.fixture(autouse=True)
def clean_db():
    PaymentTransaction.objects.delete()
    Booking.objects.delete()
    SlotLock.objects.delete()
    Charger.objects.delete()
    User.objects.delete()
    yield
    PaymentTransaction.objects.delete()
    Booking.objects.delete()
    SlotLock.objects.delete()
    Charger.objects.delete()
    User.objects.delete()


@pytest.fixture
def payment_setup():
    host = register_user(
        email="host.pay@evshare.in",
        password="Password123!",
        full_name="Payment Host",
        role="host"
    )
    driver = register_user(
        email="driver.pay@evshare.in",
        password="Password123!",
        full_name="Payment Driver",
        role="driver"
    )
    charger = create_charger(
        host=host,
        title="Payment Test Charger",
        description="Testing payments",
        charger_type="DC",
        connector_types=["CCS2"],
        power_kw=50.0,
        price_per_kwh=16.0,
        city="Greater Noida",
        display_address="KM 10",
        lat=28.4000,
        lng=77.5200
    )
    charger.verification_status = "approved"
    charger.is_active = True
    charger.save()

    slot_start = datetime.now(timezone.utc) + timedelta(days=1)
    slot_end = slot_start + timedelta(hours=1)
    booking = create_booking(driver=driver, charger=charger, slot_start_dt=slot_start, slot_end_dt=slot_end)

    return host, driver, charger, booking

def test_simulated_payment_creation(payment_setup):
    """Verify transaction generation with itemized fee and simulation watermark."""
    host, driver, charger, booking = payment_setup
    
    txn = create_or_get_transaction(booking, driver)
    assert txn is not None
    assert txn.is_simulation is True
    assert txn.status == "initiated"
    assert txn.platform_commission == booking.pricing_snapshot.platform_fee
    assert txn.host_payout_amount == booking.pricing_snapshot.subtotal_amount
    assert txn.amount == booking.pricing_snapshot.total_amount

def test_simulated_payment_success_workflow(payment_setup):
    """Verify successful simulated payment updates booking state."""
    host, driver, charger, booking = payment_setup
    
    txn = create_or_get_transaction(booking, driver)
    success = process_simulated_payment(txn, outcome="success")
    
    assert success is True
    txn.reload()
    assert txn.status == "successful"
    assert txn.paid_at is not None
    
    booking.reload()
    assert booking.payment_status == "simulated_paid"

def test_simulated_payment_failure_workflow(payment_setup):
    """Verify failed simulated payment does not mark booking as paid."""
    host, driver, charger, booking = payment_setup
    
    txn = create_or_get_transaction(booking, driver)
    success = process_simulated_payment(txn, outcome="failed")
    
    assert success is False
    txn.reload()
    assert txn.status == "failed"
    
    booking.reload()
    assert booking.payment_status != "simulated_paid"

def test_simulated_refund_workflow(payment_setup):
    """Verify refund transitions status to refunded."""
    host, driver, charger, booking = payment_setup
    
    txn = create_or_get_transaction(booking, driver)
    process_simulated_payment(txn, outcome="success")
    
    refund_success = refund_simulated_payment(txn, reason="Trip cancelled")
    assert refund_success is True
    txn.reload()
    assert txn.status == "refunded"
    assert txn.refunded_at is not None
