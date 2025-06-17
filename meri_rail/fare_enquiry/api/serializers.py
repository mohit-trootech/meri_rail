from utils.utils import get_model
from utils.serializers import (
    DynamicModelSerializer,
    DateFromToBaseSerializer,
    TrainNumberBaseSerializer,
)
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer
from rest_framework.serializers import (
    DateField,
    CharField,
    ChoiceField,
)
from utils.constants import TrainQuota, JourneyClass, AppLabelsModel, DD_MM_YYYY

Fare = get_model(**AppLabelsModel.FARE)
FareBreakDown = get_model(**AppLabelsModel.FARE_BREAKDOWN)
Train = get_model(**AppLabelsModel.TRAIN)
Station = get_model(**AppLabelsModel.STATION)


class FareEnquirySerializer(DateFromToBaseSerializer, TrainNumberBaseSerializer):
    train = CharField(required=True)
    dt = DateField(required=True)
    from_station = CharField(required=True)
    to_station = CharField(required=True)
    train_cls = ChoiceField(required=True, choices=JourneyClass.get_choice())
    quota = ChoiceField(required=True, choices=TrainQuota.get_choice())

    def validate_dt(self, value):
        value = super().validate_dt(value)
        return value.strftime(DD_MM_YYYY)

    def validate_train(self, value):
        value = super().validate_train(value)
        return value.name_number_format


class FareBreakDownSerializer(DynamicModelSerializer):
    class Meta:
        model = FareBreakDown
        fields = (
            "base_fare",
            "reservation_charge",
            "superfast_charge",
            "total_concession",
            "tatkal_fare",
            "gst_charge",
            "other_charge",
            "catering_charge",
            "dynamic_fare",
        )


class FareSerializer(DynamicModelSerializer):
    train = TrainSerializer(read_only=True)
    from_station = StationSerializer(read_only=True)
    to_station = StationSerializer(read_only=True)
    breakdown = FareBreakDownSerializer()

    class Meta:
        model = Fare
        fields = (
            "train",
            "from_station",
            "to_station",
            "distance",
            "total_fare",
            "quota",
            "train_cls",
            "breakdown",
        )
        extra_kwargs = {
            "breakdown": {"read_only": True},
            "train": {"read_only": True},
            "from_station": {"read_only": True},
            "to_station": {"read_only": True},
        }

    def create(self, validated_data):
        breakdown = validated_data.pop("breakdown")
        instance = super().create(validated_data)
        FareBreakDown.objects.create(fare=instance, **breakdown)
        return instance
