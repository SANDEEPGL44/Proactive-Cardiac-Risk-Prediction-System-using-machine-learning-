"""
WSGI config for health_desease project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for 'health_desease'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_desease.settings')

# Get the WSGI application for deployment
application = get_wsgi_application()
