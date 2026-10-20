"""
Django settings for EV Share project.
Target: Python 3.12, Django 6.1, MongoDB via MongoEngine.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent
FRONTEND_DIR = REPO_DIR / 'frontend'

# Load environment variables from backend/.env or root .env
if (BASE_DIR / '.env').exists():
    load_dotenv(BASE_DIR / '.env')
elif (REPO_DIR / '.env').exists():
    load_dotenv(REPO_DIR / '.env')

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'evshare-dev-secret-key-3.12-safe')

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [h.strip() for h in os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',') if h.strip()]
if 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

# Application definition
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sessions',
    
    # Custom EV Share modular monolith applications
    'core',
    'accounts',
    'chargers',
    'bookings',
    'sessions_app',
    'payments',
    'reviews',
    'support',
    'administration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Custom MongoEngine user session loader
    'accounts.middleware.MongoAuthMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Locate templates in frontend/templates/ (or backend/templates/ if co-located)
TEMPLATE_DIRS = [FRONTEND_DIR / 'templates', BASE_DIR / 'templates']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [p for p in TEMPLATE_DIRS if p.exists()],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.app_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database configuration:
# MongoDB + MongoEngine is the primary application database.
# Django ORM backend is configured with dummy backend to eliminate relational database dependency.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Session engine:
# Using cryptographically signed cookies to store session state in the browser.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'evshare_session'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400 * 7  # 7 days
SESSION_COOKIE_SECURE = not DEBUG

# Internationalization
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) located in frontend/static/
STATIC_URL = '/static/'
STATIC_DIRS = [FRONTEND_DIR / 'static', BASE_DIR / 'static']
STATICFILES_DIRS = [p for p in STATIC_DIRS if p.exists()]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files for uploaded KYC and charger photos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

# Email backend (console logging for local development)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@evshare.in')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Map Tile Configuration (CARTO Positron default — Apple-quiet, high contrast, unblocked)
MAP_TILE_URL = os.getenv('MAP_TILE_URL', 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png')
MAP_TILE_ATTRIBUTION = os.getenv('MAP_TILE_ATTRIBUTION', '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_blank" rel="noopener">CARTO</a>')
MAP_TILE_SUBDOMAINS = os.getenv('MAP_TILE_SUBDOMAINS', 'abcd')
MAP_TILE_MAX_ZOOM = int(os.getenv('MAP_TILE_MAX_ZOOM', '19'))

# Production Security Defaults
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

