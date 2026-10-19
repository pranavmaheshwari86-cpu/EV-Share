"""
Reviews views - Driver review submission view.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from bookings.documents import Booking
from reviews.documents import Review
from reviews.services import submit_review
from accounts.decorators import login_required_mongo

@login_required_mongo
def submit_review_view(request, booking_ref):
    """
    Review submission form for a completed booking.
    """
    user = request.current_user
    booking = Booking.objects(booking_reference=booking_ref.strip()).first()
    if not booking:
        raise Http404("Booking not found.")
        
    if str(user.id) != str(booking.driver.id):
        messages.error(request, "Only the driver for this booking can write a review.")
        return redirect('bookings:detail', booking_ref=booking.booking_reference)
        
    if booking.status != 'completed':
        messages.warning(request, "You can review this charger once your visit is completed.")
        return redirect('bookings:detail', booking_ref=booking.booking_reference)
        
    existing_review = Review.objects(booking=booking).first()
    if existing_review:
        messages.info(request, "You have already submitted a review for this booking.")
        return redirect('chargers:detail', charger_id=str(booking.charger.id))

    if request.method == 'POST':
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '').strip()
        try:
            submit_review(booking, user, rating=rating, comment=comment)
            messages.success(request, "Thank you! Your feedback helps other drivers along the corridor.")
            return redirect('chargers:detail', charger_id=str(booking.charger.id))
        except (ValueError, PermissionError) as err:
            messages.error(request, str(err))
            
    context = {
        'booking': booking,
        'page_title': f"Review Charger — Booking {booking.booking_reference}",
    }
    return render(request, 'reviews/submit_review.html', context)
