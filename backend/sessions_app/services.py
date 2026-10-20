"""
Sessions services - Manual charging visit start/stop logging, meter tracking, and issue reporting.
"""
from datetime import datetime, timezone
from sessions_app.documents import ChargingSession
from core.services import log_audit_event

def start_charging_session(booking, actor_user, meter_start=0.0, notes=""):
    """
    Records arrival and initiation of the charging session.
    Updates booking status to 'in_progress'.
    """
    actor_id = str(actor_user.id)
    if actor_id not in (str(booking.driver.id), str(booking.host.id)) and not actor_user.is_superuser:
        raise PermissionError("Only the assigned driver or host can start the charging session.")
        
    session = ChargingSession.objects(booking=booking).first()
    if not session:
        session = ChargingSession(
            booking=booking,
            charger=booking.charger,
            driver=booking.driver,
            host=booking.host,
            meter_start_kwh=float(meter_start or 0.0),
            session_status='started',
            is_manual_entry=True,
            start_notes=notes.strip() if notes else "",
            started_at=datetime.now(timezone.utc)
        )
        session.save()
    else:
        session.meter_start_kwh = float(meter_start or session.meter_start_kwh)
        session.session_status = 'started'
        session.start_notes = notes.strip() if notes else session.start_notes
        session.save()
        
    booking.status = 'in_progress'
    booking.updated_at = datetime.now(timezone.utc)
    booking.save()
    
    log_audit_event(
        actor_id=actor_user.id,
        actor_email=actor_user.email,
        action="session_started",
        target_type="ChargingSession",
        target_id=session.id,
        details={"booking": booking.booking_reference, "meter_start": meter_start}
    )
    return session

def end_charging_session(session, actor_user, meter_end=0.0, notes=""):
    """
    Records unplugging / completion of charging visit.
    Computes delta kWh delivered and marks booking as completed.
    """
    actor_id = str(actor_user.id)
    if actor_id not in (str(session.driver.id), str(session.host.id)) and not actor_user.is_superuser:
        raise PermissionError("Only the assigned driver or host can complete the charging session.")
        
    end_val = float(meter_end or 0.0)
    actual_kwh = max(0.0, round(end_val - session.meter_start_kwh, 2)) if end_val > 0 else session.booking.pricing_snapshot.estimated_energy_kwh
    
    session.meter_end_kwh = end_val
    session.actual_energy_kwh = actual_kwh
    session.session_status = 'completed'
    session.end_notes = notes.strip() if notes else ""
    session.completed_at = datetime.now(timezone.utc)
    session.updated_at = datetime.now(timezone.utc)
    session.save()
    
    session.booking.status = 'completed'
    session.booking.updated_at = datetime.now(timezone.utc)
    session.booking.save()
    
    log_audit_event(
        actor_id=actor_user.id,
        actor_email=actor_user.email,
        action="session_completed",
        target_type="ChargingSession",
        target_id=session.id,
        details={"booking": session.booking.booking_reference, "actual_kwh": actual_kwh}
    )
    return session

def report_session_issue(session, actor_user, issue_description):
    """
    Marks session as disputed or aborted and escalates to support.
    """
    session.session_status = 'disputed'
    session.issue_reported = issue_description.strip()
    session.updated_at = datetime.now(timezone.utc)
    session.save()
    
    session.booking.status = 'disputed'
    session.booking.updated_at = datetime.now(timezone.utc)
    session.booking.save()
    
    # Auto-generate a SupportCase
    from support.services import create_support_ticket
    ticket = create_support_ticket(
        user=actor_user,
        subject=f"Charging Dispute on Booking {session.booking.booking_reference}",
        category="session_problem",
        description=issue_description,
        related_booking=session.booking
    )
    
    log_audit_event(
        actor_id=actor_user.id,
        actor_email=actor_user.email,
        action="session_disputed",
        target_type="ChargingSession",
        target_id=session.id,
        details={"ticket": ticket.ticket_id, "issue": issue_description}
    )
    return session
