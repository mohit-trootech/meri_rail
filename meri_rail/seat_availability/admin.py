from django.contrib.admin import register, ModelAdmin
from utils.utils import get_model
from utils.constants import AppLabelsModel

SeatAvailability = get_model(**AppLabelsModel.SEAT_AVAILABILITY)


@register(SeatAvailability)
class SeatAvailabilityAdmin(ModelAdmin):
    list_display = ("train", "dt", "available", "created")
    list_filter = ("dt",)
    search_fields = ("train__name", "train__number")
    readonly_fields = ("created", "modified")
