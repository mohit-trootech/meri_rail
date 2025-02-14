from django.utils.translation import gettext_lazy as _


class ValidationErrorsConstants:
    INVALID_PNR_NUMBER = _("Please enter a valid PNR number")


class ModelVerbose:
    PNR = _("Pnr")
    PASSENGERS = _("Passengers")
