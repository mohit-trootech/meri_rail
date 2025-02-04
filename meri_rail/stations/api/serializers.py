from utils.serializers import DynamicModelSerializer
from utils.utils import get_model

Station = get_model(app_label="stations", model_name="Station")
Utterance = get_model(app_label="stations", model_name="Utterance")


class UtteranceSerializer(DynamicModelSerializer):
    class Meta:
        model = Utterance
        fields = ("name",)


class StationSerializer(DynamicModelSerializer):
    utterances = UtteranceSerializer(many=True, read_only=True)

    class Meta:
        model = Station
        fields = (
            "name",
            "code",
            "name_hi",
            "district",
            "state",
            "latitude",
            "longitude",
            "address",
            "trains_count",
            "utterances",
        )
