"""
Core URL routing.
"""
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('safety/', views.safety_guidelines_view, name='safety'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('cancellation/', views.cancellation_policy_view, name='cancellation'),
    path('health/', views.health_check_view, name='health_check'),
]
