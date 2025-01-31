from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os.path import join


class Fixtures:
    TRAIN_FIXTURE = join(settings.BASE_DIR, "fixtures/trains/trains.json")
    TRAIN_DETAILS_FIXTURE = join(settings.BASE_DIR, "fixtures/trains/details/")
    STATION_FIXTURE = join(settings.BASE_DIR, "fixtures/stations/stations.json")
    POPULAR_FIXTURE = join(settings.BASE_DIR, "fixtures/stations/popular.json")
    INVALID_FIXTURE_REGION = join(
        settings.BASE_DIR, "fixtures/stations/invalid_region.json"
    )
    INVALID_FIXTURE_CITY = join(
        settings.BASE_DIR, "fixtures/stations/invalid_city.json"
    )


class ManagementHelp:
    DUMP_TRAIN_FIXTURE = _("Load train data from JSON file")
    DUMP_TRAIN_DETAILS = _("Fetch details from Selenium and Load data")
    DUMP_STATION_FIXTURE = _("Load station data from JSON file")
    DUMP_INVALID_STATION_FIXTURE = _("Load invalid station data from JSON file")


class Messages:
    INVALID_STATIONS_DUMPED = _("Successfully loaded stations data, took %.6f")
    STATIONS_DUMPED = _("Successfully loaded invalid stations data, took %.6f")
    TRAINS_DUMPED = _("Successfully loaded trains data, took %.6f")
    TRAINS_DUMPED = _("Successfully loaded trains details, took %.6f")
