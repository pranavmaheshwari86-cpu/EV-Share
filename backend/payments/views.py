"""
Payments views - Simulated payment checkout portal and transaction receipt.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from bookings.documents import Booking
from payments.documents import PaymentTransaction
from payments.services import create_or_get_transaction, process_simulated_payment
from accounts.decorators import login_required_mongo

@login_required_mongo
def checkout_view(request, booking_ref):
    """
    Simulated Payment Checkout Portal:
    Demonstrates payment gateway authorization with explicit pilot simulation disclaimers.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    if str(user.id) != str(booking.driver.id) and not user.is_superuser:
        messages.error(request, "Only the booking driver can complete payment.")
        return redirect('bookings:detail', booking_ref=booking.booking_reference)
        
    if booking.payment_status == 'simulated_paid':
        messages.info(request, "This booking has already been paid for in simulated mode.")
        return redirect('bookings:detail', booking_ref=booking.booking_reference)

    transaction = create_or_get_transaction(booking, user)
    
    if request.method == 'POST':
        outcome = request.POST.get('outcome', 'success')
        process_simulated_payment(transaction, outcome=outcome)
        
        if outcome == 'success':
            messages.success(request, f"Simulated payment of ₹{transaction.amount:.2f} completed successfully!")
            return redirect('payments:receipt', transaction_ref=transaction.transaction_reference)
        else:
            messages.error(request, "Simulated payment failed as requested for testing.")
            return redirect('payments:receipt', transaction_ref=transaction.transaction_reference)

    context = {
        'booking': booking,
        'transaction': transaction,
        'page_title': f"Simulated Checkout — {booking.booking_reference}",
    }
    return render(request, 'payments/checkout.html', context)

@login_required_mongo
def receipt_view(request, transaction_ref):
    """
    Transaction receipt showing server-calculated breakdown and simulation watermarks.
    """
    user = request.current_user
    transaction = PaymentTransaction.objects(transaction_reference=transaction_ref.strip()).first()
    if not transaction:
        raise Http404("Transaction not found.")
        
    is_driver = str(user.id) == str(transaction.driver.id)
    is_host = str(user.id) == str(transaction.host.id)
    is_admin = user.is_superuser or 'admin' in user.roles
    
    if not (is_driver or is_host or is_admin):
        messages.error(request, "You are not authorized to view this transaction receipt.")
        return redirect('home')
        
    context = {
        'transaction': transaction,
        'booking': transaction.booking,
        'page_title': f"Payment Receipt — {transaction.transaction_reference}",
    }
    return render(request, 'payments/receipt.html', context)
