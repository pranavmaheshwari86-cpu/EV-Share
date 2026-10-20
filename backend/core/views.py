"""
Core Views - Public marketing, static informational pages, and system health checks.
"""
from django.shortcuts import render
from django.http import JsonResponse
from config.database import get_db_status

def home_view(request):
    """
    Landing page: Apple India-inspired quiet aesthetic,
    featuring authentic corridor charging nodes, value props, and transparent pilot metrics.
    """
    from chargers.documents import Charger
    try:
        featured_chargers = Charger.objects(
            verification_status='approved',
            is_active=True
        ).limit(6)
    except Exception:
        featured_chargers = []
        
    context = {
        'featured_chargers': featured_chargers,
        'page_title': 'EV Share — Peer-to-Peer EV Charging Marketplace',
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html', {'page_title': 'About EV Share'})

def how_it_works_view(request):
    return render(request, 'core/how_it_works.html', {'page_title': 'How EV Share Works'})

def safety_guidelines_view(request):
    return render(request, 'core/safety.html', {'page_title': 'Safety Guidelines & Electrical Standards'})

def terms_view(request):
    return render(request, 'core/terms.html', {'page_title': 'Terms of Service'})

def privacy_view(request):
    return render(request, 'core/privacy.html', {'page_title': 'Privacy Notice & Address Disclosure Policy'})

def cancellation_policy_view(request):
    return render(request, 'core/cancellation.html', {'page_title': 'Cancellation & Refund Policy'})

def health_check_view(request):
    status = get_db_status()
    return JsonResponse({
        'status': 'healthy',
        'platform': 'EV Share',
        'database': status,
        'pilot_corridor': 'Yamuna Expressway (Delhi-Agra)',
    })
