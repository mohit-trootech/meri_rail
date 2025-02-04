from django.contrib.admin import ModelAdmin, register, StackedInline
from utils.utils import get_model

Station = get_model(app_label="stations", model_name="Station")
Uttrance = get_model(app_label="stations", model_name="Utterance")


class UtteranceAdmin(StackedInline):
    model = Uttrance
    fk_name = "station"
    extra = 0


@register(Station)
class StationAdmin(ModelAdmin):
    list_display = ("name", "code", "district", "state")
    search_fields = ("name", "code")
    list_filter = ("state",)
    ordering = ("code", "name")
    readonly_fields = ("trains_count", "latitude", "longitude")
    inlines = (UtteranceAdmin,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "code",
                    "name_hi",
                    "trains_count",
                )
            },
        ),
        (
            "Address",
            {
                "fields": (
                    "district",
                    "state",
                    "latitude",
                    "longitude",
                    "address",
                )
            },
        ),
    )
