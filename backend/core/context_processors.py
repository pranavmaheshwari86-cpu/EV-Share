"""
Core Context Processor - Injects user identity, roles, and platform status into all templates.
"""
from django.conf import settings
from config.database import get_db_status

def app_context(request):
    current_user = getattr(request, 'current_user', None)
    is_authenticated = current_user is not None
    
    roles = current_user.roles if is_authenticated else []
    
    return {
        'current_user': current_user,
        'is_authenticated': is_authenticated,
        'is_driver': 'driver' in roles,
        'is_host': 'host' in roles,
        'is_admin': 'admin' in roles or (current_user and current_user.is_superuser),
        'db_status': get_db_status(),
        'PILOT_CORRIDOR_NAME': 'Yamuna Expressway (Delhi NCR – Agra)',
        'PLATFORM_NAME': 'EV Share',
        'PLATFORM_TAGLINE': 'Your Charger. Someone Else’s Journey. Everyone Benefits.',
        'MAP_TILE_URL': getattr(settings, 'MAP_TILE_URL', 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}'),
        'MAP_TILE_ATTRIBUTION': getattr(settings, 'MAP_TILE_ATTRIBUTION', 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, METI, TomTom'),
        'MAP_TILE_SUBDOMAINS': getattr(settings, 'MAP_TILE_SUBDOMAINS', ''),
        'MAP_TILE_MAX_ZOOM': getattr(settings, 'MAP_TILE_MAX_ZOOM', 19),
    }
