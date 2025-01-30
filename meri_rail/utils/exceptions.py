"""Custom Exceptions Cases for PNR Scrapping"""

from rest_framework.serializers import ValidationError


class PNRNotFound(ValidationError):
    """PNR Not Found Base Exceptions"""

    pass


class InvalidPnrNumber(ValidationError):
    """Invalid PNR Number Exception"""

    pass
