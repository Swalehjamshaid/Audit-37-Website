# ... your existing settings (keep INSTALLED_APPS with 'webaudit', etc.) ...

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Standard Django

# Production settings for Railway
DEBUG = False
ALLOWED_HOSTS = ['*']  # Secure later with your domain

# Static files (for report.html, CSS, etc.)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # If you have a static/ folder
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# If using DB (Railway Postgres)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT'),
    }
}

# Ensure 'webaudit' is in INSTALLED_APPS (add if missing)
INSTALLED_APPS = [
    # ... your existing apps ...
    'webaudit',  # This auto-registers your local webaudit app
    # ... 
]

# Logging for debugging (optional — check Railway logs)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
