from utils.utils import get_model
from utils.serializers import DynamicModelSerializer
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer
from utils.serializers import DateFromToBaseSerializer

TrainsList = get_model(app_label="trains_between_station", model_name="TrainsList")
TrainBetweenStation = get_model(
    app_label="trains_between_station", model_name="TrainBetweenStation"
)
Station = get_model(app_label="stations", model_name="Station")


class TbisSerializer(DateFromToBaseSerializer):
    pass


class TrainsBetweenStationSerializer(DynamicModelSerializer):
    from_station = StationSerializer(many=False, read_only=True)
    to_station = StationSerializer(many=False, read_only=True)

    class Meta:
        model = TrainBetweenStation
        fields = ("from_station", "to_station")


class TrainListSerializer(DynamicModelSerializer):
    train = TrainSerializer(many=False, read_only=True)
    train_between_station = TrainsBetweenStationSerializer(many=False, read_only=True)

    class Meta:
        model = TrainsList
        fields = (
            "train",
            "train_between_station",
            "arrival_time",
            "departure_time",
            "distance",
            "duration",
            "train_type",
            "on_monday",
            "on_tuesday",
            "on_wednesday",
            "on_thursday",
            "on_friday",
            "on_saturday",
            "on_sunday",
        )
