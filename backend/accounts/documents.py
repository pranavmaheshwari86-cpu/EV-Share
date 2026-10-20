"""
Accounts documents - User identity, vehicles, and host onboarding verification.
"""
from datetime import datetime, timezone
import mongoengine as me

class Vehicle(me.EmbeddedDocument):
    make = me.StringField(required=True)  # e.g., Tata, MG, Mahindra, Hyundai, BYD
    model = me.StringField(required=True)  # e.g., Nexon EV, ZS EV, XUV400, Ioniq 5
    registration_number = me.StringField(required=True)  # e.g., DL-01-AB-1234
    connector_type = me.StringField(required=True, choices=['CCS2', 'Type 2', 'GB/T', '15A 3-Pin'])
    battery_capacity_kwh = me.FloatField(default=30.0)

    def __str__(self):
        return f"{self.make} {self.model} ({self.registration_number})"

class User(me.Document):
    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['email'], 'unique': True},
            'roles',
            'is_active',
        ]
    }

    full_name = me.StringField(required=True, max_length=120)
    email = me.EmailField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    phone_number = me.StringField(max_length=20)
    roles = me.ListField(me.StringField(choices=['driver', 'host', 'admin']), default=lambda: ['driver'])
    vehicles = me.EmbeddedDocumentListField(Vehicle)
    is_active = me.BooleanField(default=True)
    is_verified_host = me.BooleanField(default=False)
    is_superuser = me.BooleanField(default=False)
    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def clean(self):
        if self.email:
            self.email = self.email.strip().lower()

    def has_role(self, role):
        if self.is_superuser:
            return True
        return role in self.roles

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class HostVerification(me.Document):
    meta = {
        'collection': 'host_verifications',
        'indexes': [
            'user',
            'status',
            '-submitted_at'
        ]
    }

    user = me.ReferenceField('User', required=True, reverse_delete_rule=me.CASCADE)
    host_type = me.StringField(
        required=True,
        choices=[
            'residential',
            'commercial_hotel',
            'commercial_restaurant',
            'commercial_office',
            'commercial_parking',
            'other'
        ]
    )
    business_name = me.StringField()
    contact_phone = me.StringField(required=True)
    property_address = me.StringField(required=True)
    id_proof_type = me.StringField(
        required=True,
        choices=['aadhaar', 'pan', 'gstin', 'electricity_bill', 'other']
    )
    id_proof_number = me.StringField(required=True)
    id_proof_file = me.StringField()  # Relative media file path or placeholder
    property_permission_file = me.StringField()
    safety_declaration_agreed = me.BooleanField(default=False)
    status = me.StringField(
        default='submitted',
        choices=['draft', 'submitted', 'under_review', 'approved', 'rejected', 'changes_requested']
    )
    admin_notes = me.StringField()
    reviewed_by = me.StringField()
    reviewed_at = me.DateTimeField()
    submitted_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return f"HostVerification for {self.user.email} - [{self.status}]"
