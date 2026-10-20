"""
Payments services - Simulated transaction processing, fee separation, and refunds.
"""
import random
import string
from datetime import datetime, timezone
from payments.documents import PaymentTransaction
from core.services import log_audit_event

def generate_transaction_reference():
    suffix = "".join(random.choices(string.ascii_uppercase + "0123456789", k=8))
    return f"TXN-SIM-{suffix}"

def create_or_get_transaction(booking, driver):
    """
    Creates or reuses an initiated transaction for the given booking.
    """
    txn = PaymentTransaction.objects(booking=booking, status__in=['initiated', 'pending']).first()
    if txn:
        return txn
        
    total = booking.pricing_snapshot.total_amount
    subtotal = booking.pricing_snapshot.subtotal_amount
    platform_fee = booking.pricing_snapshot.platform_fee
    host_payout = round(subtotal, 2)
    
    ref = generate_transaction_reference()
    while PaymentTransaction.objects(transaction_reference=ref).first():
        ref = generate_transaction_reference()
        
    txn = PaymentTransaction(
        transaction_reference=ref,
        booking=booking,
        driver=driver,
        host=booking.host,
        amount=total,
        currency='INR',
        platform_commission=platform_fee,
        host_payout_amount=host_payout,
        provider='simulated_sandbox',
        status='initiated',
        is_simulation=True,
        created_at=datetime.now(timezone.utc)
    )
    txn.save()
    return txn

def process_simulated_payment(transaction, outcome='success'):
    """
    Simulates outcome of payment gateway authorization.
    """
    if outcome == 'success':
        transaction.status = 'successful'
        transaction.paid_at = datetime.now(timezone.utc)
        transaction.save()
        
        transaction.booking.payment_status = 'simulated_paid'
        transaction.booking.updated_at = datetime.now(timezone.utc)
        transaction.booking.save()
        
        log_audit_event(
            actor_id=transaction.driver.id,
            actor_email=transaction.driver.email,
            action="payment_simulated_success",
            target_type="PaymentTransaction",
            target_id=transaction.id,
            details={"ref": transaction.transaction_reference, "amount": transaction.amount}
        )
    else:
        transaction.status = 'failed'
        transaction.save()
        log_audit_event(
            actor_id=transaction.driver.id,
            actor_email=transaction.driver.email,
            action="payment_simulated_failed",
            target_type="PaymentTransaction",
            target_id=transaction.id,
            details={"ref": transaction.transaction_reference, "amount": transaction.amount}
        )
    return transaction.status == 'successful'

def refund_simulated_payment(transaction, reason="Booking cancelled"):
    """
    Simulates refund processing for cancelled or disputed bookings.
    """
    transaction.status = 'refunded'
    transaction.refunded_at = datetime.now(timezone.utc)
    transaction.save()

    transaction.booking.payment_status = 'refunded'
    transaction.booking.updated_at = datetime.now(timezone.utc)
    transaction.booking.save()

    log_audit_event(
        actor_id=transaction.driver.id,
        actor_email=transaction.driver.email,
        action="payment_simulated_refunded",
        target_type="PaymentTransaction",
        target_id=transaction.id,
        details={"ref": transaction.transaction_reference, "reason": reason}
    )
    return True

