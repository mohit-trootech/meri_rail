from meri_rail.settings.celery_conf import app as celery_app  # noqa

__all__ = ("celery_app",)
default_app_config = "meri_rail.apps.MeriRailConfig"
