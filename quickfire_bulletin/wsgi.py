"""
WSGI config for quickfire_bulletin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickfire_bulletin.settings')

# Get the base application
application = get_wsgi_application()

# Use WhiteNoise for serving static files
application = WhiteNoise(application)
