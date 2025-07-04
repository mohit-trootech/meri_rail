from django.utils.translation import gettext_lazy as _

TRAIN_BETWEEN_STATION = "from %s to %s"
TRAINS_LIST = "%s- %s"
TBIS_CACHE_KEY = "tbis_%(from_station)s-%(to_station)s-%(dt)s"


class ModelVebose:
    TRAIN_BETWEEN_STATION = _("Trains between stations")
    TRAINS_LIST = _("Trains List")
