from django.contrib.admin import register, ModelAdmin, StackedInline
from utils.utils import get_model
from utils.constants import AppLabelsModel

Train = get_model(**AppLabelsModel.TRAIN)
TrainDetail = get_model(**AppLabelsModel.TRAIN_DETAIL)
Schedule = get_model(**AppLabelsModel.SCHEDULE)
Route = get_model(**AppLabelsModel.ROUTE)


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
