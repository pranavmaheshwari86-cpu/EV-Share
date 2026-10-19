"""
Core documents - Audit logs and platform events.
"""
from datetime import datetime, timezone
import mongoengine as me

class AuditEvent(me.Document):
    meta = {
        'collection': 'audit_logs',
        'indexes': [
            '-timestamp',
            'actor_id',
            'action',
            'target_type',
        ]
    }
    
    actor_id = me.StringField(required=True)
    actor_email = me.StringField()
    action = me.StringField(required=True)  # e.g., 'host_approved', 'charger_suspended', 'booking_cancelled'
    target_type = me.StringField(required=True)  # e.g., 'User', 'Charger', 'Booking', 'Review'
    target_id = me.StringField(required=True)
    details = me.DictField(default=dict)
    ip_address = me.StringField()
    timestamp = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.actor_email}: {self.action} on {self.target_type}({self.target_id})"
