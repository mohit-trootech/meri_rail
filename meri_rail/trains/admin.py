from django.contrib.admin import register, ModelAdmin
from utils.utils import get_model


Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


@register(Train)
class TrainAdmin(ModelAdmin):
    pass


@register(TrainDetail)
class TrainDetailAdmin(ModelAdmin):
    list_display = ("train", "train__name", "train__number")
    search_fields = ("train__name",)


@register(Schedule)
class ScheduleAdmin(ModelAdmin):
    pass


@register(Route)
class RouteAdmin(ModelAdmin):
    pass
