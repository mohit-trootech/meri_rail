from utils.serializers import DynamicModelSerializer
from utils.utils import get_model


Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


class RouteSerializer(DynamicModelSerializer):
    class Meta:
        model = Route
        fields = (
            "station",
            "route_number",
            "halt",
            "day_count",
            "platform",
            "arrival",
            "departure",
        )


class ScheduleSerializer(DynamicModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        )


class TrainDetailSerializer(DynamicModelSerializer):
    class Meta:
        model = TrainDetail
        fields = (
            "station_from",
            "station_to",
            "distance",
        )


class TrainSerializer(DynamicModelSerializer):
    details = TrainDetailSerializer(many=False, read_only=True)
    schedule = ScheduleSerializer(many=False, read_only=True)
    route = RouteSerializer(many=True, read_only=True)

    class Meta:
        model = Train
        fields = (
            "number",
            "name",
            "details",
            "schedule",
            "route",
        )
