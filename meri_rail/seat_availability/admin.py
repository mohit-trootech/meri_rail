from django.contrib.admin import register, ModelAdmin
from utils.utils import get_model

SeatAvailability = get_model(
    app_label="seat_availability", model_name="SeatAvailability"
)


@register(SeatAvailability)
class SeatAvailabilityAdmin(ModelAdmin):
    list_display = ("train", "dt", "available", "created")
    list_filter = ("dt",)
    search_fields = ("train__name", "train__number")
    readonly_fields = ("created", "modified")
