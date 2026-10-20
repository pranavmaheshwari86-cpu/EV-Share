"""
Sessions URL routing.
"""
from django.urls import path
from sessions_app import views

app_name = 'sessions_app'

urlpatterns = [
    path('<str:booking_ref>/start/', views.start_session_view, name='start'),
    path('<str:booking_ref>/complete/', views.end_session_view, name='complete'),
    path('<str:booking_ref>/report-issue/', views.report_issue_view, name='report_issue'),
]
