"""
Chargers documents - Charger specifications, address, schedules, and GeoJSON location.
"""
from datetime import datetime, timezone
import mongoengine as me

class AvailabilityRule(me.EmbeddedDocument):
    """
    Weekly recurring availability rule (day 0=Monday to 6=Sunday).
    """
    day_of_week = me.IntField(required=True, min_value=0, max_value=6)
    start_time = me.StringField(required=True, default="08:00")  # "HH:MM" 24h
    end_time = me.StringField(required=True, default="20:00")

    def day_name(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[self.day_of_week] if 0 <= self.day_of_week <= 6 else 'Unknown'

    def __str__(self):
        return f"{self.day_name()}: {self.start_time} - {self.end_time}"

class BlackoutPeriod(me.EmbeddedDocument):
    """
    Specific date blackout when charger is unavailable.
    """
    date = me.StringField(required=True)  # "YYYY-MM-DD"
    reason = me.StringField(default="Host unavailable")

    def __str__(self):
        return f"{self.date} ({self.reason})"

class ChargerAddress(me.EmbeddedDocument):
    """
    Address details distinguishing public display from protected private directions.
    """
    city = me.StringField(required=True)
    state = me.StringField(default='Uttar Pradesh')
    postal_code = me.StringField()
    display_address = me.StringField(required=True)  # Public, e.g. "Near Jewar Interchange, Yamuna Expressway"
    private_directions = me.StringField()  # Disclosed ONLY after booking confirmation!

    def __str__(self):
        return f"{self.display_address}, {self.city}"

class Charger(me.Document):
    meta = {
        'collection': 'chargers',
        'indexes': [
            [('location', '2dsphere')],
            'host',
            'verification_status',
            'is_active',
            'charger_type',
            'price_per_kwh',
        ]
    }

    host = me.ReferenceField('accounts.User', required=True, reverse_delete_rule=me.CASCADE)
    title = me.StringField(required=True, max_length=150)
    description = me.StringField(required=True)
    charger_type = me.StringField(required=True, choices=['AC', 'DC'])
    connector_types = me.ListField(me.StringField(choices=['CCS2', 'Type 2', 'GB/T', '15A 3-Pin']), required=True)
    power_output_kw = me.FloatField(required=True, min_value=1.0)
    price_per_kwh = me.FloatField(required=True, min_value=0.0)
    currency = me.StringField(default='INR')
    
    address = me.EmbeddedDocumentField(ChargerAddress, required=True)
    location = me.PointField(required=True)  # [longitude, latitude]
    
    amenities = me.ListField(me.StringField(), default=list)  # Restrooms, WiFi, Cafe, Security, Covered
    photos = me.ListField(me.StringField(), default=list)  # URLs / local filenames
    
    availability_rules = me.EmbeddedDocumentListField(AvailabilityRule)
    blackout_periods = me.EmbeddedDocumentListField(BlackoutPeriod)
    
    verification_status = me.StringField(
        default='pending',
        choices=['draft', 'pending', 'approved', 'rejected', 'suspended']
    )
    is_active = me.BooleanField(default=True)
    
    average_rating = me.FloatField(default=0.0)
    reviews_count = me.IntField(default=0)
    
    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    @property
    def is_bookable(self):
        return self.verification_status == 'approved' and self.is_active

    @property
    def longitude(self):
        if self.location:
            if isinstance(self.location, dict) and 'coordinates' in self.location:
                return self.location['coordinates'][0]
            elif isinstance(self.location, (list, tuple)) and len(self.location) >= 2:
                return float(self.location[0])
        return None

    @property
    def latitude(self):
        if self.location:
            if isinstance(self.location, dict) and 'coordinates' in self.location:
                return self.location['coordinates'][1]
            elif isinstance(self.location, (list, tuple)) and len(self.location) >= 2:
                return float(self.location[1])
        return None

    def __str__(self):
        return f"{self.title} ({self.power_output_kw} kW {self.charger_type}) [{self.verification_status}]"
