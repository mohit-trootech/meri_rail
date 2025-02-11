from django.contrib.admin import ModelAdmin, register, StackedInline
from utils.utils import get_model

Fare = get_model(app_label="fare_enquiry", model_name="Fare")
FareBreakDown = get_model(app_label="fare_enquiry", model_name="FareBreakDown")


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
