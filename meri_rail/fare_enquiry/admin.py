from django.contrib.admin import ModelAdmin, register, StackedInline
from utils.utils import get_model
from utils.constants import AppLabelsModel

Fare = get_model(**AppLabelsModel.FARE)
FareBreakDown = get_model(**AppLabelsModel.FARE_BREAKDOWN)


class FareBreakDownInline(StackedInline):
    model = FareBreakDown
    fk_name = "fare"


@register(Fare)
class FareAdmin(ModelAdmin):
    inlines = [FareBreakDownInline]
    list_display = (
        "train",
        "from_station__code",
        "to_station__code",
        "quota",
        "train_cls",
        "total_fare",
    )
