from django.contrib import admin
from utils.utils import get_model


Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


admin.site.register(Train)
admin.site.register(TrainDetail)
admin.site.register(Schedule)
admin.site.register(Route)
