import os
import django

# Initialize Django for pytest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
