from django.apps import AppConfig
from utils.selenium_service import SeleniumService


class MeriRailConfig(AppConfig):
    name = "meri_rail"

    def ready(self):
        SeleniumService()
