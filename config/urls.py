"""
EV Share root URL configuration.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('chargers/', include('chargers.urls')),
    path('bookings/', include('bookings.urls')),
    path('sessions/', include('sessions_app.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('support/', include('support.urls')),
    path('admin-portal/', include('administration.urls')),
    path('administration/', include('administration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
