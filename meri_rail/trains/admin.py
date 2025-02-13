from django.contrib.admin import register, ModelAdmin, StackedInline
from utils.utils import get_model


Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


class ScheduleInline(StackedInline):
    model = Schedule
    fk_name = "train"
    extra = 0


class TrainDetailsInline(StackedInline):
    model = TrainDetail
    fk_name = "train"
    extra = 0


class RouteInline(StackedInline):
    model = Route
    fk_name = "train"
    extra = 0


@register(Train)
class TrainAdmin(ModelAdmin):
    list_display = ("name", "number", "details__distance")
    search_fields = ("name", "number")
    ordering = ("number",)
    fields = ("number", "name")
    inlines = (ScheduleInline, TrainDetailsInline, RouteInline)
