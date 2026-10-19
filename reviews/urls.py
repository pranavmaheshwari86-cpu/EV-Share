"""
Reviews URL routing.
"""
from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('submit/<str:booking_ref>/', views.submit_review_view, name='submit'),
]
