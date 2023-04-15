"""
WSGI config for gpt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""


import os, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gpt.settings')

application = get_wsgi_application()
