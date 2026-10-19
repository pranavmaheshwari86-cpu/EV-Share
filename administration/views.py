"""
Administration views - Operations dashboard, host verification, listing moderation, user management, and audit inspection.
"""
from datetime import datetime, timezone
from bson import ObjectId
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from accounts.documents import User, HostVerification
from accounts.services import approve_host_verification, reject_host_verification
from chargers.documents import Charger
from bookings.documents import Booking
from payments.documents import PaymentTransaction
from support.documents import SupportCase
from support.services import resolve_support_ticket
from core.documents import AuditEvent
from core.services import log_audit_event
from accounts.decorators import login_required_mongo, role_required_mongo

@login_required_mongo
@role_required_mongo('admin')
def admin_dashboard_view(request):
    """
    Overview operational dashboard: platform counts, queues, and activity.
    """
    total_users = User.objects.count()
    total_hosts = User.objects(roles='host').count()
    pending_verifications = HostVerification.objects(status__in=['submitted', 'under_review']).count()
    
    total_chargers = Charger.objects.count()
    approved_chargers = Charger.objects(verification_status='approved', is_active=True).count()
    pending_chargers = Charger.objects(verification_status='pending').count()
    
    total_bookings = Booking.objects.count()
    completed_bookings = Booking.objects(status='completed').count()
    active_disputes = SupportCase.objects(status__in=['open', 'in_progress']).count()
    
    # Financial simulation totals
    simulated_txns = list(PaymentTransaction.objects(status='successful'))
    sim_gross_gmv = sum(t.amount for t in simulated_txns)
    sim_platform_comm = sum(t.platform_commission for t in simulated_txns)
    sim_host_payouts = sum(t.host_payout_amount for t in simulated_txns)
    
    recent_audit = AuditEvent.objects.order_by('-timestamp').limit(8)
    
    context = {
        'total_users': total_users,
        'total_hosts': total_hosts,
        'pending_verifications': pending_verifications,
        'total_chargers': total_chargers,
        'approved_chargers': approved_chargers,
        'pending_chargers': pending_chargers,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'active_disputes': active_disputes,
        'sim_gross_gmv': sim_gross_gmv,
        'sim_platform_comm': sim_platform_comm,
        'sim_host_payouts': sim_host_payouts,
        'recent_audit': recent_audit,
        'page_title': 'Admin Operations Portal — EV Share',
    }
    return render(request, 'administration/dashboard.html', context)

@login_required_mongo
@role_required_mongo('admin')
def host_verifications_view(request):
    """
    Queue of host verification KYC applications.
    """
    status_filter = request.GET.get('status', 'submitted')
    if status_filter == 'all':
        verifications = HostVerification.objects.order_by('-submitted_at')
    else:
        verifications = HostVerification.objects(status=status_filter).order_by('-submitted_at')
        
    context = {
        'verifications': verifications,
        'current_filter': status_filter,
        'page_title': 'Host KYC Verification Queue — Admin',
    }
    return render(request, 'administration/host_verifications.html', context)

@login_required_mongo
@role_required_mongo('admin')
def verify_host_action_view(request, verification_id):
    """
    Approve or reject host onboarding verification.
    """
    user = request.current_user
    action = request.POST.get('action')
    notes = request.POST.get('admin_notes', '')
    
    try:
        if action == 'approve':
            approve_host_verification(verification_id, user, admin_notes=notes)
            messages.success(request, "Host verification approved successfully! Host can now list chargers.")
        elif action == 'reject':
            reject_host_verification(verification_id, user, reason=notes)
            messages.warning(request, "Host verification rejected.")
    except Exception as exc:
        messages.error(request, f"Error processing verification: {exc}")
        
    return redirect('administration:host_verifications')

@login_required_mongo
@role_required_mongo('admin')
def charger_moderation_view(request):
    """
    Queue of charger listings needing approval or review.
    """
    status_filter = request.GET.get('status', 'pending')
    if status_filter == 'all':
        chargers = Charger.objects.order_by('-created_at')
    else:
        chargers = Charger.objects(verification_status=status_filter).order_by('-created_at')
        
    context = {
        'chargers': chargers,
        'current_filter': status_filter,
        'page_title': 'Charger Listing Moderation — Admin',
    }
    return render(request, 'administration/charger_moderation.html', context)

@login_required_mongo
@role_required_mongo('admin')
def moderate_charger_action_view(request, charger_id):
    """
    Approve, reject, or suspend a charger listing.
    """
    user = request.current_user
    action = request.POST.get('action')
    try:
        charger = Charger.objects(id=ObjectId(charger_id)).first()
        if not charger:
            raise Http404("Charger not found.")
            
        if action == 'approve':
            charger.verification_status = 'approved'
            charger.is_active = True
            messages.success(request, f"Charger '{charger.title}' approved and published!")
        elif action == 'reject':
            charger.verification_status = 'rejected'
            charger.is_active = False
            messages.warning(request, f"Charger '{charger.title}' rejected.")
        elif action == 'suspend':
            charger.verification_status = 'suspended'
            charger.is_active = False
            messages.warning(request, f"Charger '{charger.title}' suspended.")
            
        charger.updated_at = datetime.now(timezone.utc)
        charger.save()
        
        log_audit_event(
            actor_id=user.id,
            actor_email=user.email,
            action=f"charger_{action}d",
            target_type="Charger",
            target_id=charger.id,
            details={"title": charger.title}
        )
    except Exception as exc:
        messages.error(request, f"Error updating listing: {exc}")
        
    return redirect('administration:charger_moderation')

@login_required_mongo
@role_required_mongo('admin')
def booking_inspector_view(request):
    """
    Inspector for all platform bookings, slot allocations, and payment states.
    """
    bookings = Booking.objects.order_by('-created_at').limit(50)
    context = {
        'bookings': bookings,
        'page_title': 'Platform Booking Inspector — Admin',
    }
    return render(request, 'administration/booking_inspector.html', context)

@login_required_mongo
@role_required_mongo('admin')
def user_management_view(request):
    """
    View and manage all registered users and roles.
    """
    users = User.objects.order_by('-created_at')
    context = {
        'users': users,
        'page_title': 'User Management & Permissions — Admin',
    }
    return render(request, 'administration/users.html', context)

@login_required_mongo
@role_required_mongo('admin')
def toggle_user_status_view(request, user_id):
    """
    Suspend or reactivate a user account.
    """
    admin_user = request.current_user
    target_user = User.objects(id=ObjectId(user_id)).first()
    if target_user:
        if target_user.is_superuser:
            messages.error(request, "Cannot suspend a platform superuser.")
        else:
            target_user.is_active = not target_user.is_active
            target_user.save()
            status_word = "Activated" if target_user.is_active else "Suspended"
            messages.info(request, f"User {target_user.email} is now {status_word}.")
            log_audit_event(
                actor_id=admin_user.id,
                actor_email=admin_user.email,
                action=f"user_{status_word.lower()}",
                target_type="User",
                target_id=target_user.id,
                details={"target_email": target_user.email}
            )
    return redirect('administration:users')

@login_required_mongo
@role_required_mongo('admin')
def disputes_queue_view(request):
    """
    Dispute and support ticket investigation queue.
    """
    tickets = SupportCase.objects.order_by('-created_at')
    context = {
        'tickets': tickets,
        'page_title': 'Support & Dispute Queue — Admin',
    }
    return render(request, 'administration/disputes.html', context)

@login_required_mongo
@role_required_mongo('admin')
def resolve_dispute_action_view(request, ticket_id):
    """
    Resolves a dispute with resolution notes.
    """
    admin_user = request.current_user
    ticket = SupportCase.objects(ticket_id=ticket_id.strip()).first()
    if ticket:
        notes = request.POST.get('resolution_notes', '').strip()
        resolve_support_ticket(ticket, admin_user, resolution_notes=notes)
        messages.success(request, f"Ticket {ticket.ticket_id} resolved.")
    return redirect('administration:disputes')

@login_required_mongo
@role_required_mongo('admin')
def audit_logs_view(request):
    """
    Review historical platform audit events.
    """
    logs = AuditEvent.objects.order_by('-timestamp').limit(100)
    context = {
        'logs': logs,
        'page_title': 'Platform Audit Logs — Admin',
    }
    return render(request, 'administration/audit_logs.html', context)
