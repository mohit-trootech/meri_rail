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
from django.db import IntegrityError

SeatAvailability = get_model(**AppLabelsModel.SEAT_AVAILABILITY)
Train = get_model(**AppLabelsModel.TRAIN)
Station = get_model(**AppLabelsModel.STATION)
TrainClass = get_model(**AppLabelsModel.TRAIN_CLASS)


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
        train = Train.objects.get(number=self.context["request"].data["train"])
        from_station = Station.objects.get(
            code=self.context["request"].data["from_station"].upper()
        )
        to_station = Station.objects.get(
            code=self.context["request"].data["to_station"].upper()
        )
        validated_data.update(
            {
                "train_id": train.id,
                "from_station_id": from_station.id,
                "to_station_id": to_station.id,
            }
        )
        try:
            instance = super().create(validated_data)
            if not instance.train.journey_class.filter(name=instance.train_cls):
                instance.train.journey_class.add(
                    TrainClass.objects.get(name=instance.train_cls).id
                )
        except IntegrityError:
            instance = SeatAvailability.objects.get(
                train=train,
                from_station=from_station,
                to_station=to_station,
                dt=validated_data["dt"],
                quota=validated_data["quota"],
                train_cls=validated_data["train_cls"],
            )
        return super().update(instance, validated_data)
