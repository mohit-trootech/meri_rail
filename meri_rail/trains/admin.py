from django.contrib.admin import ModelAdmin, register
from utils.utils import get_model

Train = get_model(app_label="trains", model_name="Train")


@register(Train)
class TrainAdmin(ModelAdmin):
    list_display = ("number", "name")
    search_fields = ("number", "name")
    ordering = ("name", "number")
    readonly_fields = ("number",)
