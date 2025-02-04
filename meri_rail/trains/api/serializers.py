from utils.serializers import DynamicModelSerializer
from utils.utils import get_model
from stations.api.serializers import StationSerializer

Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


class RouteSerializer(DynamicModelSerializer):
    station = StationSerializer(many=False, read_only=True)

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


class TrainSerializer(DynamicModelSerializer):
    class Meta:
        model = Train
        fields = (
            "number",
            "name",
        )


class TrainDetailViewSerializer(TrainSerializer):
    schedule = ScheduleSerializer(many=False, read_only=True)
    route = RouteSerializer(many=True, read_only=True)

    class Meta(TrainSerializer.Meta):
        fields = (
            "number",
            "name",
            "schedule",
            "route",
        )


class TrainDetailSerializer(DynamicModelSerializer):
    train = TrainDetailViewSerializer(many=False, read_only=True)
    station_from = StationSerializer(many=False, read_only=True)
    station_to = StationSerializer(many=False, read_only=True)

    class Meta:
        model = TrainDetail
        fields = (
            "train",
            "station_from",
            "station_to",
            "distance",
        )
