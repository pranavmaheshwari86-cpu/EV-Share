"""
EV Share root URL configuration.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('chargers/', include('chargers.urls')),
    path('bookings/', include('bookings.urls')),
    path('sessions/', include('sessions_app.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('support/', include('support.urls')),
    path('administration/', include('administration.urls')),
    path('admin-portal/', RedirectView.as_view(url='/administration/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
