"""
Support documents - SupportCase for user inquiries, disputes, and incident reports.
"""
from datetime import datetime, timezone
import mongoengine as me

class SupportCase(me.Document):
    meta = {
        'collection': 'support_cases',
        'indexes': [
            {'fields': ['ticket_id'], 'unique': True},
            'user',
            'related_booking',
            'category',
            'status',
            '-created_at',
        ]
    }

    ticket_id = me.StringField(required=True, unique=True)
    user = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    related_booking = me.ReferenceField('bookings.Booking', reverse_delete_rule=me.NULLIFY)
    
    subject = me.StringField(required=True, max_length=150)
    category = me.StringField(
        required=True,
        choices=[
            'session_problem',
            'payment_issue',
            'charger_misleading',
            'safety_concern',
            'general_query'
        ]
    )
    description = me.StringField(required=True)
    status = me.StringField(
        default='open',
        choices=['open', 'in_progress', 'resolved', 'closed']
    )
    
    resolution_notes = me.StringField()
    resolved_by = me.StringField()
    resolved_at = me.DateTimeField()

    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"Ticket {self.ticket_id}: {self.subject} [{self.status}]"
