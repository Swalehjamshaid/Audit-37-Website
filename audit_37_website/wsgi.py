import os
import sys

# CRITICAL FIX: Add project root to sys.path so 'webaudit' is found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit_37_website.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
