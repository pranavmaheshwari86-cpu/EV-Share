"""
Support URL routing.
"""
from django.urls import path
from support import views

app_name = 'support'

urlpatterns = [
    path('', views.ticket_list_view, name='list'),
    path('new/', views.create_ticket_view, name='create'),
    path('<str:ticket_id>/', views.ticket_detail_view, name='detail'),
]
