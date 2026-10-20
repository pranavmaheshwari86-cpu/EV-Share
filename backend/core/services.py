"""
Core services - Audit logging and shared helpers.
"""
import logging
from datetime import datetime, timezone
from core.documents import AuditEvent

logger = logging.getLogger(__name__)

def log_audit_event(actor_id, actor_email, action, target_type, target_id, details=None, ip_address=None):
    """
    Persist an administrative or security audit event.
    """
    try:
        event = AuditEvent(
            actor_id=str(actor_id),
            actor_email=actor_email or "system",
            action=action,
            target_type=target_type,
            target_id=str(target_id),
            details=details or {},
            ip_address=ip_address,
            timestamp=datetime.now(timezone.utc)
        )
        event.save()
        logger.info(f"[AUDIT] {action} by {actor_email} on {target_type} ({target_id})")
        return event
    except Exception as exc:
        logger.error(f"[AUDIT ERROR] Failed to record audit event: {exc}")
        return None

def format_currency_inr(amount):
    """
    Format float/int amount to Indian currency standard (e.g. ₹240.00).
    """
    try:
        return f"₹{float(amount):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"
