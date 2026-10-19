"""
Bookings documents - Concurrency locks, pricing snapshots, and booking lifecycle records.
"""
from datetime import datetime, timezone
import mongoengine as me

class PricingSnapshot(me.EmbeddedDocument):
    """
    Immutable pricing snapshot captured at time of booking confirmation.
    """
    rate_per_kwh = me.FloatField(required=True)
    estimated_energy_kwh = me.FloatField(required=True)
    subtotal_amount = me.FloatField(required=True)
    platform_fee = me.FloatField(required=True)
    gst_amount = me.FloatField(default=0.0)
    total_amount = me.FloatField(required=True)
    currency = me.StringField(default='INR')

    def __str__(self):
        return f"₹{self.total_amount:.2f} ({self.estimated_energy_kwh} kWh @ ₹{self.rate_per_kwh}/kWh)"

class SlotLock(me.Document):
    """
    Atomic concurrency barrier for exclusive charger time slots.
    Guarantees no two bookings can ever reserve the same (charger, slot_start).
    """
    meta = {
        'collection': 'slot_locks',
        'indexes': [
            {'fields': ['charger', 'slot_start'], 'unique': True},
            'booking_ref',
            'locked_at',
        ]
    }

    charger = me.ReferenceField('chargers.Charger', required=True, reverse_delete_rule=me.CASCADE)
    slot_start = me.DateTimeField(required=True)
    slot_end = me.DateTimeField(required=True)
    booking_ref = me.StringField()
    locked_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"Lock on {self.charger.title} @ {self.slot_start.strftime('%Y-%m-%d %H:%M')}"

class Booking(me.Document):
    meta = {
        'collection': 'bookings',
        'indexes': [
            {'fields': ['booking_reference'], 'unique': True},
            'driver',
            'host',
            'charger',
            'status',
            'slot_start',
            '-created_at',
        ]
    }

    booking_reference = me.StringField(required=True, unique=True)
    driver = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    host = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    charger = me.ReferenceField('chargers.Charger', required=True, reverse_delete_rule=me.CASCADE)
    vehicle = me.EmbeddedDocumentField('accounts.Vehicle')
    
    slot_start = me.DateTimeField(required=True)
    slot_end = me.DateTimeField(required=True)
    
    pricing_snapshot = me.EmbeddedDocumentField(PricingSnapshot, required=True)
    
    status = me.StringField(
        default='confirmed',
        choices=[
            'pending',
            'confirmed',
            'in_progress',
            'completed',
            'cancelled',
            'expired',
            'disputed'
        ]
    )
    payment_status = me.StringField(
        default='unpaid',
        choices=['unpaid', 'simulated_paid', 'refunded']
    )
    
    cancellation_reason = me.StringField()
    cancelled_by = me.StringField()
    cancelled_at = me.DateTimeField()
    
    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    @property
    def duration_hours(self):
        delta = self.slot_end - self.slot_start
        return max(1.0, round(delta.total_seconds() / 3600.0, 1))

    @property
    def is_cancellable(self):
        return self.status in ('pending', 'confirmed')

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.charger.title} [{self.status}]"
