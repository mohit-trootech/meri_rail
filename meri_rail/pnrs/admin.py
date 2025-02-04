from django.contrib.admin import ModelAdmin, register, StackedInline
from utils.utils import get_model

Pnr = get_model(app_label="pnrs", model_name="Pnr")
Passengers = get_model(app_label="pnrs", model_name="Passengers")


class PassengersInline(StackedInline):
    model = Passengers
    extra = 3
    show_change_link = True


@register(Pnr)
class PnrAdmin(ModelAdmin):
    list_display = (
        "pnr",
        "date_of_journey",
        "train__number",
        "source__code",
        "destination__code",
        "boarding__code",
    )
    search_fields = ("pnr", "train__number")
    list_filter = ("date_of_journey",)
    inlines = (PassengersInline,)
