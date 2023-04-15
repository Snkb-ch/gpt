"""
WSGI config for gpt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""


import os, sys
sys.path.insert(0, '/var/www/u2019785/data/www/brainstormai.ru/gpt')
sys.path.insert(1, '/var/www/u2019785/data/djangoenv/lib/python3.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gpt.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()