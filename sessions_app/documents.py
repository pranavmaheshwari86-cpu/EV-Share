"""
ChargingSession document - Records physical charging visit events and manual meter evidence.
"""
from datetime import datetime, timezone
import mongoengine as me

class ChargingSession(me.Document):
    meta = {
        'collection': 'charging_sessions',
        'indexes': [
            {'fields': ['booking'], 'unique': True},
            'charger',
            'driver',
            'host',
            'session_status',
            '-started_at',
        ]
    }

    booking = me.ReferenceField('bookings.Booking', required=True, unique=True, reverse_delete_rule=me.CASCADE)
    charger = me.ReferenceField('chargers.Charger', required=True, reverse_delete_rule=me.CASCADE)
    driver = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    host = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)

    session_status = me.StringField(
        default='started',
        choices=['started', 'completed', 'aborted', 'disputed']
    )
    
    meter_start_kwh = me.FloatField(default=0.0)
    meter_end_kwh = me.FloatField(default=0.0)
    actual_energy_kwh = me.FloatField(default=0.0)
    
    # Transparency requirement: explicitly label manual data vs. hardware telemetry
    is_manual_entry = me.BooleanField(default=True)
    telemetry_label = me.StringField(default="Manual Host Entry — Unverified Telemetry")

    started_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    completed_at = me.DateTimeField()
    
    start_notes = me.StringField()
    end_notes = me.StringField()
    issue_reported = me.StringField()

    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"Session for Booking {self.booking.booking_reference} [{self.session_status}]"
