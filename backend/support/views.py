"""
Support views - Ticket creation and status tracking.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from support.documents import SupportCase
from support.services import create_support_ticket
from accounts.decorators import login_required_mongo

@login_required_mongo
def create_ticket_view(request):
    """
    User support request / inquiry submission view.
    """
    user = request.current_user
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        category = request.POST.get('category', 'general_query')
        description = request.POST.get('description', '').strip()
        booking_ref = request.POST.get('booking_ref', '').strip()
        
        related_booking = None
        if booking_ref:
            from bookings.documents import Booking
            related_booking = Booking.objects(booking_reference=booking_ref).first()
            
        if not subject or not description:
            messages.error(request, "Please enter both subject and description.")
        else:
            ticket = create_support_ticket(
                user=user,
                subject=subject,
                category=category,
                description=description,
                related_booking=related_booking
            )
            messages.success(request, f"Support ticket {ticket.ticket_id} created. Our operations team will follow up.")
            return redirect('support:list')
            
    context = {
        'page_title': 'Contact EV Share Support — Help & Grievances',
    }
    return render(request, 'support/create_ticket.html', context)

@login_required_mongo
def ticket_list_view(request):
    """
    List user's submitted support cases.
    """
    user = request.current_user
    tickets = SupportCase.objects(user=user).order_by('-created_at')
    
    context = {
        'tickets': tickets,
        'page_title': 'My Support Tickets — EV Share',
    }
    return render(request, 'support/ticket_list.html', context)

@login_required_mongo
def ticket_detail_view(request, ticket_id):
    """
    View status and resolution notes of a support case.
    """
    user = request.current_user
    ticket = SupportCase.objects(ticket_id=ticket_id.strip()).first()
    if not ticket:
        raise Http404("Ticket not found.")
        
    if str(ticket.user.id) != str(user.id) and not (user.is_superuser or 'admin' in user.roles):
        messages.error(request, "You do not have permission to view this ticket.")
        return redirect('home')
        
    context = {
        'ticket': ticket,
        'page_title': f"Ticket {ticket.ticket_id} — EV Share Support",
    }
    return render(request, 'support/ticket_detail.html', context)
