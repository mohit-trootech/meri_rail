from utils.utils import get_model
from trains.api.serializers import TrainSerializer
from utils.serializers import (
    DynamicModelSerializer,
    DateFromToBaseSerializer,
    TrainNumberBaseSerializer,
)
from rest_framework.serializers import ChoiceField
from utils.constants import JourneyClass, TrainQuota, AppLabelsModel, DD_MM_YYYY
from rest_framework import serializers
from stations.api.serializers import StationSerializer

SeatAvailability = get_model(**AppLabelsModel.SEAT_AVAILABILITY)
Train = get_model(**AppLabelsModel.TRAIN)
Station = get_model(**AppLabelsModel.STATION)


class SeatAvailabilityFilterSerializer(
    TrainNumberBaseSerializer, DateFromToBaseSerializer
):
    quota = ChoiceField(required=True, choices=TrainQuota.get_choice())
    train_cls = ChoiceField(required=True, choices=JourneyClass.get_choice())

    def validate_train(self, value):
        value = super().validate_train(value)
        return value.name_number_format

    def validate_dt(self, value):
        value = super().validate_dt(value)
        return value.strftime(DD_MM_YYYY)


class CustomListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        instance_mapping = {item.dt: item for item in instance}
        data_mapping = {item["dt"]: item for item in validated_data}

        instances = []
        for item_key, data in data_mapping.items():
            item = instance_mapping.get(item_key, None)
            if item is None:
                instances.append(self.child.create(data))
            else:
                instances.append(self.child.update(item, data))

        for item_key, item in instance_mapping.items():
            if item_key not in data_mapping:
                item.delete()

        return instances


class SeatAvailabilitySerializer(DynamicModelSerializer):
    train = TrainSerializer(many=False, read_only=True)
    from_station = StationSerializer(many=False, read_only=True)
    to_station = StationSerializer(many=False, read_only=True)

    class Meta:
        model = SeatAvailability
        fields = (
            "train",
            "dt",
            "from_station",
            "to_station",
            "available",
            "created",
            "modified",
            "quota",
            "train_cls",
        )
        list_serializer_class = CustomListSerializer

    def create(self, validated_data):
        validated_data.update(
            {
                "train_id": Train.objects.get(
                    number=self.context["request"].data["train"]
                ).id,
                "from_station_id": Station.objects.get(
                    code=self.context["request"].data["from_station"].upper()
                ).id,
                "to_station_id": Station.objects.get(
                    code=self.context["request"].data["to_station"].upper()
                ).id,
            }
        )
        return super().create(validated_data)
