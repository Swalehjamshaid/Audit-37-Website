import os
import sys
from pathlib import Path

# Add project root to path so 'webaudit' is found
sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit_37_website.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
