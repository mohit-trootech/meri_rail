from django.apps import AppConfig


class SeatAvailabilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "seat_availability"

    def ready(self):
        super().ready()
        import seat_availability.signals  # noqa
