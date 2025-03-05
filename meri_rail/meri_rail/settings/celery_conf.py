import os
from celery import Celery
from dotenv import dotenv_values
from django.conf import settings

env = dotenv_values(".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.get("DJANGO_SETTINGS_MODULE"))

app = Celery("meri_rail")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
