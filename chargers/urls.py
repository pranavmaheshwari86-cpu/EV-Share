"""
Chargers URL routing.
"""
from django.urls import path
from chargers import views

app_name = 'chargers'

urlpatterns = [
    path('', views.search_chargers_view, name='search'),
    path('urgent-assistance/', views.low_battery_view, name='low_battery'),
    path('my-listings/', views.host_charger_list_view, name='host_list'),
    path('mine/', views.host_charger_list_view, name='mine'),
    path('new/', views.create_charger_view, name='create'),
    path('<str:charger_id>/', views.charger_detail_view, name='detail'),
    path('<str:charger_id>/edit/', views.edit_charger_view, name='edit'),
    path('<str:charger_id>/toggle/', views.toggle_charger_status_view, name='toggle'),
    path('<str:charger_id>/slots/', views.api_available_slots_view, name='api_slots'),
]
