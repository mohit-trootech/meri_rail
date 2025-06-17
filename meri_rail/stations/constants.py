from django.utils.translation import gettext_lazy as _

STATION_NAME_CODE_VALID_FORMAT = "%s+-+%s"
STATION_CACHE_KEY = "station-%s"


class ModelVerbose:
    STATION = _("Station")
    STATIONS = _("Stations")

    UTTERANCE = _("Utterance")
    UTTERANCES = _("Utterances")
