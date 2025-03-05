"""
WSGI config for meri_rail project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv import dotenv_values
from django.core.wsgi import get_wsgi_application

env = dotenv_values(".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.get("DJANGO_SETTINGS_MODULE"))

application = get_wsgi_application()
