"""
ASGI config for meri_rail project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from dotenv import dotenv_values
from django.core.asgi import get_asgi_application

env = dotenv_values(".env")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.get("DJANGO_SETTINGS_MODULE"))

application = get_asgi_application()
