from django.utils.translation import gettext_lazy as _


class ValidationErrorsConstants:
    INVALID_PNR_NUMBER = _("Please enter a valid PNR number")


class ModelVerbose:
    PNR = _("Pnr")
    PASSENGERS = _("Passengers")


class EventBody:
    TITLE = "PNR: {pnr} | Train: {train[name]} - {train[number]}"
    DESCRIPTION = "PNR: {pnr} | Train: {train[number]} | Source: {source[name]} - {source[code]} | Destination: {destination[name]} - {destination[code]} | Boarding: {boarding[name]} - {boarding[code]} | Journey Class: {journey_class} | Chart Status: {chart_status} | Cancel Status: {cancel_status} | Quota: {quota} | Distance: {distance} KMs"
    LOCATION = "{source[name]} - {source[code]} | {source[name_hi]} | {source[address]}"
    DATE_TIME = "%sT%s"
