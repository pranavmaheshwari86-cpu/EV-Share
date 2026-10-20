"""
Reviews documents - Review entity with uniqueness per completed booking.
"""
from datetime import datetime, timezone
import mongoengine as me

class Review(me.Document):
    meta = {
        'collection': 'reviews',
        'indexes': [
            {'fields': ['booking'], 'unique': True},
            'charger',
            'driver',
            'rating',
            '-created_at',
        ]
    }

    booking = me.ReferenceField('bookings.Booking', required=True, unique=True, reverse_delete_rule=me.CASCADE)
    charger = me.ReferenceField('chargers.Charger', required=True, reverse_delete_rule=me.CASCADE)
    driver = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)

    rating = me.IntField(required=True, min_value=1, max_value=5)
    comment = me.StringField(required=True, max_length=1000)
    
    is_moderated = me.BooleanField(default=False)
    is_visible = me.BooleanField(default=True)
    moderation_reason = me.StringField()

    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"Review by {self.driver.full_name} for {self.charger.title} ({self.rating}★)"
