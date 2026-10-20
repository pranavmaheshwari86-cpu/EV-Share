"""
Payments documents - PaymentTransaction records and simulation metadata.
"""
from datetime import datetime, timezone
import mongoengine as me

class PaymentTransaction(me.Document):
    meta = {
        'collection': 'payment_transactions',
        'indexes': [
            {'fields': ['transaction_reference'], 'unique': True},
            'booking',
            'driver',
            'host',
            'status',
            '-created_at',
        ]
    }

    transaction_reference = me.StringField(required=True, unique=True)
    booking = me.ReferenceField('bookings.Booking', required=True, reverse_delete_rule=me.CASCADE)
    driver = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    host = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)

    amount = me.FloatField(required=True)
    currency = me.StringField(default='INR')
    
    platform_commission = me.FloatField(default=0.0)
    host_payout_amount = me.FloatField(default=0.0)
    
    provider = me.StringField(default='simulated_sandbox')
    status = me.StringField(
        default='initiated',
        choices=['initiated', 'pending', 'successful', 'failed', 'refunded']
    )
    
    is_simulation = me.BooleanField(default=True)
    simulation_watermark = me.StringField(default="PILOT SIMULATION — NO REAL MONEY TRANSFERRED")

    paid_at = me.DateTimeField()
    refunded_at = me.DateTimeField()

    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"Payment {self.transaction_reference} - ₹{self.amount:.2f} [{self.status}]"
