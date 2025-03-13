from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os.path import join


class RequestTypes:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"

    CHOICES = (
        (GET, "GET"),
        (POST, "POST"),
        (PUT, "PUT"),
        (DELETE, "DELETE"),
        (PATCH, "PATCH"),
    )

    @classmethod
    def get_choices(cls):
        return cls.CHOICES


class Fixtures:
    TRAIN_FIXTURE = join(settings.BASE_DIR, "fixtures/trains/trains.json")
    INVALID_TRAIN_FIXTURE = join(
        settings.BASE_DIR, "fixtures/trains/invalid_trains.json"
    )
    TRAIN_DETAILS_FIXTURE = join(settings.BASE_DIR, "fixtures/trains/details/%s.json")
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
    DUMP_TRAIN_DETAILS_FIXTURE = _("Dump train details data from JSON file")
    DUMP_TRAIN_DETAILS = _("Fetch details from Selenium and Load data")
    DUMP_STATION_FIXTURE = _("Load station data from JSON file")
    DUMP_INVALID_STATION_FIXTURE = _("Load invalid station data from JSON file")


class Messages:
    STATIONS_DUMPED = _("Successfully loaded stations data, took %.6f")
    INVALID_STATIONS_DUMPED = _("Successfully loaded invalid stations data, took %.6f")
    TRAINS_DUMPED = _("Successfully loaded trains data, took %.6f")
    TRAINS_DETAILS_DUMPED = _("Successfully loaded trains details, took %.6f")
    TRAINS_DETAILS_FETCHED = _("Successfully fetched trains details, took %.6f")


class ModelVerbose:
    NOTIFICATION = _("Notification")
    NOTIFICATIONS = _("Notifications")

    EMAIL_TEMPLATE = _("Email Template")
    EMAIL_TEMPLATES = _("Email Templates")


class EmailType:
    REGISTRATION_SUCCESS = "registration_success"
    VERIFICATION_PENDING = "verification_pending"
    VERIFICATION_DONE = "verification_done"
    PNR_STATUS = "pnr_status"
    SEAT_AVAILABILITY = "seat_availability"
    TRAIN_STATUS = "train_status"
    PASSWORD_RESET = "password_reset"
    PASSWORD_RESET_DONE = "password_reset_done"
    PASSWORD_FORGOT = "password_forgot"

    CHOICES = (
        (REGISTRATION_SUCCESS, _("Registration Success")),
        (VERIFICATION_PENDING, _("Verification Pending")),
        (VERIFICATION_DONE, _("Verification Done")),
        (PNR_STATUS, _("PNR Status")),
        (SEAT_AVAILABILITY, _("Seat Availability")),
        (TRAIN_STATUS, _("Train Status")),
        (PASSWORD_RESET, _("Password Reset")),
        (PASSWORD_RESET_DONE, _("Password Reset Done")),
        (PASSWORD_FORGOT, _("Password Forgot")),
    )

    @classmethod
    def get_choices(cls):
        return cls.CHOICES


class ErrorMessages:
    CHOICE_CLASS_NOT_SET = _("choice_class must be set")
