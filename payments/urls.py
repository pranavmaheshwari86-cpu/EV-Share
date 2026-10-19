"""
Payments URL routing.
"""
from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    path('checkout/<str:booking_ref>/', views.checkout_view, name='checkout'),
    path('receipt/<str:transaction_ref>/', views.receipt_view, name='receipt'),
]
