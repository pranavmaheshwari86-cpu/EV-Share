"""
Administration URL routing.
"""
from django.urls import path
from administration import views

app_name = 'administration'

urlpatterns = [
    path('', views.admin_dashboard_view, name='dashboard'),
    path('verifications/', views.host_verifications_view, name='host_verifications'),
    path('verifications/<str:verification_id>/action/', views.verify_host_action_view, name='verify_host_action'),
    path('chargers/', views.charger_moderation_view, name='charger_moderation'),
    path('chargers/<str:charger_id>/action/', views.moderate_charger_action_view, name='moderate_charger_action'),
    path('bookings/', views.booking_inspector_view, name='booking_inspector'),
    path('users/', views.user_management_view, name='users'),
    path('users/<str:user_id>/toggle/', views.toggle_user_status_view, name='toggle_user'),
    path('disputes/', views.disputes_queue_view, name='disputes'),
    path('disputes/<str:ticket_id>/resolve/', views.resolve_dispute_action_view, name='resolve_dispute'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
]
