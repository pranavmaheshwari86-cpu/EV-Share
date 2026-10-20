"""
Accounts URL routing.
"""
from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('host-onboarding/', views.host_onboarding_view, name='host_onboarding'),
    path('onboarding/', views.host_onboarding_view, name='onboarding'),
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
]
