"""
Reviews services - Review submission, duplicate prevention, and average rating aggregation.
"""
from datetime import datetime, timezone
from reviews.documents import Review
from core.services import log_audit_event

def submit_review(booking, driver, rating, comment):
    """
    Submits a review for an eligible completed charging visit.
    Enforces that only the booking's driver can review and only once per booking.
    """
    if str(driver.id) != str(booking.driver.id):
        raise PermissionError("Only the driver who booked this session can submit a review.")
        
    if booking.status != 'completed':
        raise ValueError("Reviews can only be submitted for completed charging visits.")
        
    existing = Review.objects(booking=booking).first()
    if existing:
        raise ValueError("A review has already been submitted for this booking.")
        
    rating_val = int(rating)
    if not (1 <= rating_val <= 5):
        raise ValueError("Rating must be between 1 and 5 stars.")
        
    comment_clean = (comment or "").strip()
    if not comment_clean:
        raise ValueError("Please provide a brief comment describing your charging experience.")
        
    review = Review(
        booking=booking,
        charger=booking.charger,
        driver=driver,
        rating=rating_val,
        comment=comment_clean,
        is_visible=True,
        created_at=datetime.now(timezone.utc)
    )
    review.save()
    
    # Recalculate charger average rating
    charger = booking.charger
    all_reviews = list(Review.objects(charger=charger, is_visible=True))
    if all_reviews:
        avg = sum(r.rating for r in all_reviews) / len(all_reviews)
        charger.average_rating = round(avg, 1)
        charger.reviews_count = len(all_reviews)
        charger.save()
        
    log_audit_event(
        actor_id=driver.id,
        actor_email=driver.email,
        action="review_submitted",
        target_type="Review",
        target_id=review.id,
        details={"charger": charger.title, "rating": rating_val}
    )
    return review

def moderate_review(review, admin_user, is_visible=False, reason=""):
    """
    Admin action to moderate or hide abusive/inappropriate reviews.
    """
    review.is_visible = is_visible
    review.is_moderated = True
    review.moderation_reason = reason.strip()
    review.save()
    
    # Recalculate charger rating after moderation
    charger = review.charger
    visible_reviews = list(Review.objects(charger=charger, is_visible=True))
    if visible_reviews:
        avg = sum(r.rating for r in visible_reviews) / len(visible_reviews)
        charger.average_rating = round(avg, 1)
        charger.reviews_count = len(visible_reviews)
    else:
        charger.average_rating = 0.0
        charger.reviews_count = 0
    charger.save()
    
    log_audit_event(
        actor_id=admin_user.id,
        actor_email=admin_user.email,
        action="review_moderated",
        target_type="Review",
        target_id=review.id,
        details={"is_visible": is_visible, "reason": reason}
    )
    return review
