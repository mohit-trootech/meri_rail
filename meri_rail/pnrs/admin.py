from django.contrib.admin import ModelAdmin, register, StackedInline
from utils.utils import get_model
from utils.constants import AppLabelsModel

Pnr = get_model(**AppLabelsModel.PNR)
Passengers = get_model(**AppLabelsModel.PASSENGER)


class PassengersInline(StackedInline):
    model = Passengers
    fk_name = "pnr"
    extra = 0


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
    readonly_fields = ("created", "modified")
    list_filter = ("date_of_journey",)
    inlines = (PassengersInline,)
    filter_horizontal = ["users"]
