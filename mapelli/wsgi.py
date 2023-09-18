"""
WSGI config for mapelli project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mapelli.settings')

sys.path.append('home/giulio/django/mapelli')
sys.path.append('home/giulio/django/mapelli/mapelli')

application = get_wsgi_application()
