from django.contrib.admin import ModelAdmin, StackedInline, register
from utils.utils import get_model

TrainBetweenStation = get_model(
    app_label="trains_between_station", model_name="TrainBetweenStation"
)
TrainsList = get_model(app_label="trains_between_station", model_name="TrainsList")


class TrainsListInline(StackedInline):
    model = TrainsList
    extra = 0
    fk_name = "train_between_station"


@register(TrainBetweenStation)
class TrainBetweenStationAdmin(ModelAdmin):
    inlines = [TrainsListInline]
    list_display = ("from_station", "to_station")
