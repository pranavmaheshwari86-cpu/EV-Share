"""
Accounts services - Business logic for user lifecycle, authentication, and host KYC.
"""
from datetime import datetime, timezone
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
from accounts.documents import User, Vehicle, HostVerification
from core.services import log_audit_event

def create_user(full_name="", email="", password="", roles=None, phone_number=None, is_superuser=False, role=None, **kwargs):
    """
    Registers a new user with hashed password and normalized lowercase email.
    """
    if not full_name and 'name' in kwargs:
        full_name = kwargs['name']
    if not full_name:
        full_name = (email or "").split('@')[0].capitalize()

    email_clean = (email or "").strip().lower()
    if not email_clean:
        raise ValueError("Email address is required.")
        
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters.")
        
    if User.objects(email=email_clean).first():
        raise ValueError("An account with this email address already exists.")
        
    if role and not roles:
        if role == 'host':
            user_roles = ['driver', 'host']
        else:
            user_roles = [role]
    else:
        user_roles = roles or ['driver']
    
    user = User(
        full_name=full_name.strip(),
        email=email_clean,
        password_hash=make_password(password),
        phone_number=(phone_number or "").strip(),
        roles=user_roles,
        is_active=True,
        is_superuser=is_superuser,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    user.save()
    log_audit_event(
        actor_id=user.id,
        actor_email=user.email,
        action="user_registered",
        target_type="User",
        target_id=user.id,
        details={"roles": user_roles}
    )
    return user

register_user = create_user

def authenticate_user(email, password):
    """
    Authenticates email and password. Returns active User document or None.
    """
    email_clean = (email or "").strip().lower()
    if not email_clean or not password:
        return None
        
    user = User.objects(email=email_clean).first()
    if not user:
        return None
        
    if not user.is_active:
        return None
        
    if check_password(password, user.password_hash):
        return user
        
    return None

def add_vehicle(user, make, model, registration_number, connector_type, battery_kwh=30.0):
    """
    Appends a vehicle to the driver's profile.
    """
    vehicle = Vehicle(
        make=make.strip(),
        model=model.strip(),
        registration_number=registration_number.strip().upper(),
        connector_type=connector_type.strip(),
        battery_capacity_kwh=float(battery_kwh or 30.0)
    )
    user.vehicles.append(vehicle)
    user.updated_at = datetime.now(timezone.utc)
    user.save()
    return vehicle

def submit_host_verification(user, host_type, contact_phone, property_address,
                             id_proof_type, id_proof_number, business_name="",
                             id_proof_file="", property_permission_file="",
                             safety_agreed=True):
    """
    Submits a host verification application.
    """
    verification = HostVerification.objects(user=user).first()
    if not verification:
        verification = HostVerification(user=user)
        
    verification.host_type = host_type
    verification.business_name = business_name
    verification.contact_phone = contact_phone
    verification.property_address = property_address
    verification.id_proof_type = id_proof_type
    verification.id_proof_number = id_proof_number
    verification.id_proof_file = id_proof_file
    verification.property_permission_file = property_permission_file
    verification.safety_declaration_agreed = bool(safety_agreed)
    verification.status = 'submitted'
    verification.submitted_at = datetime.now(timezone.utc)
    verification.updated_at = datetime.now(timezone.utc)
    verification.save()
    
    # Automatically ensure user has 'host' role in their profile
    if 'host' not in user.roles:
        user.roles.append('host')
        user.save()
        
    log_audit_event(
        actor_id=user.id,
        actor_email=user.email,
        action="host_verification_submitted",
        target_type="HostVerification",
        target_id=verification.id,
        details={"host_type": host_type}
    )
    return verification

def approve_host_verification(verification_id, admin_user, admin_notes=""):
    """
    Approves host verification, granting verified host status.
    """
    verification = HostVerification.objects(id=ObjectId(verification_id)).first()
    if not verification:
        raise ValueError("Verification record not found.")
        
    verification.status = 'approved'
    verification.admin_notes = admin_notes
    verification.reviewed_by = admin_user.email
    verification.reviewed_at = datetime.now(timezone.utc)
    verification.updated_at = datetime.now(timezone.utc)
    verification.save()
    
    target_user = verification.user
    target_user.is_verified_host = True
    if 'host' not in target_user.roles:
        target_user.roles.append('host')
    target_user.save()
    
    log_audit_event(
        actor_id=admin_user.id,
        actor_email=admin_user.email,
        action="host_verification_approved",
        target_type="HostVerification",
        target_id=verification.id,
        details={"target_user": target_user.email}
    )
    return verification

def reject_host_verification(verification_id, admin_user, reason=""):
    """
    Rejects host verification with reason.
    """
    verification = HostVerification.objects(id=ObjectId(verification_id)).first()
    if not verification:
        raise ValueError("Verification record not found.")
        
    verification.status = 'rejected'
    verification.admin_notes = reason
    verification.reviewed_by = admin_user.email
    verification.reviewed_at = datetime.now(timezone.utc)
    verification.updated_at = datetime.now(timezone.utc)
    verification.save()
    
    log_audit_event(
        actor_id=admin_user.id,
        actor_email=admin_user.email,
        action="host_verification_rejected",
        target_type="HostVerification",
        target_id=verification.id,
        details={"reason": reason}
    )
    return verification
