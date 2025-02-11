from utils.utils import get_model
from utils.serializers import DynamicModelSerializer
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer

TrainsList = get_model(app_label="trains_between_station", model_name="TrainsList")


class TrainListSerializer(DynamicModelSerializer):
    train = TrainSerializer()
    station = StationSerializer()

    class Meta:
        model = TrainsList
        fields = (
            "train",
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
