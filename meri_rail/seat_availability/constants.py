from django.utils.translation import gettext_lazy as _

SEAT_AVAILABILITY = "%s - %s Availability"
SEAT_AVAILABILITY_CACHE = "seat_availability-%(train)s-%(quota)s-%(train_cls)s-%(dt)s-%(from_station)s-%(to_station)s"


class ModelVerbose:
    SEAT_AVAILABILITY = _("Seat Availability")
    SEATS_AVAILABILITY = _("Seats Availability")
    DATE = _("Date")
