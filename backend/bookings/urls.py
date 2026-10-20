"""
Bookings URL routing.
"""
from django.urls import path
from bookings import views

app_name = 'bookings'

urlpatterns = [
    path('history/', views.driver_booking_history_view, name='driver_history'),
    path('reservations/', views.host_reservations_view, name='host_reservations'),
    path('create/<str:charger_id>/', views.create_booking_view, name='create'),
    path('<str:booking_ref>/', views.booking_detail_view, name='detail'),
    path('<str:booking_ref>/cancel/', views.cancel_booking_view, name='cancel'),
]
