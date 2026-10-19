"""
Support services - Ticket creation, resolution, and escalation logging.
"""
import random
import string
from datetime import datetime, timezone
from support.documents import SupportCase
from core.services import log_audit_event

def generate_ticket_id():
    suffix = "".join(random.choices(string.ascii_uppercase + "123456789", k=6))
    return f"CASE-{suffix}"

def create_support_ticket(user, subject, category, description, related_booking=None):
    """
    Submits a new support or dispute ticket.
    """
    tid = generate_ticket_id()
    while SupportCase.objects(ticket_id=tid).first():
        tid = generate_ticket_id()
        
    ticket = SupportCase(
        ticket_id=tid,
        user=user,
        related_booking=related_booking,
        subject=subject.strip(),
        category=category,
        description=description.strip(),
        status='open',
        created_at=datetime.now(timezone.utc)
    )
    ticket.save()
    
    log_audit_event(
        actor_id=user.id,
        actor_email=user.email,
        action="support_ticket_created",
        target_type="SupportCase",
        target_id=ticket.id,
        details={"ticket_id": tid, "category": category}
    )
    return ticket

def resolve_support_ticket(ticket, admin_user, resolution_notes=""):
    """
    Resolves a dispute ticket.
    """
    ticket.status = 'resolved'
    ticket.resolution_notes = resolution_notes.strip()
    ticket.resolved_by = admin_user.email
    ticket.resolved_at = datetime.now(timezone.utc)
    ticket.updated_at = datetime.now(timezone.utc)
    ticket.save()
    
    log_audit_event(
        actor_id=admin_user.id,
        actor_email=admin_user.email,
        action="support_ticket_resolved",
        target_type="SupportCase",
        target_id=ticket.id,
        details={"ticket_id": ticket.ticket_id}
    )
    return ticket
