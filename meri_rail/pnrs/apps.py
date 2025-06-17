from django.apps import AppConfig


class PnrsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pnrs"

    def ready(self):
        import pnrs.signals  # noqa F401

        return super().ready()
