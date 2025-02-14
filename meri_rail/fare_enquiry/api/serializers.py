from utils.utils import get_model
from utils.serializers import DynamicModelSerializer, DateFromToBaseSerializer
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer
from rest_framework.serializers import (
    DateField,
    CharField,
    ChoiceField,
    ValidationError,
)
from utils.constants import TrainQuota, JourneyClass

Fare = get_model(app_label="fare_enquiry", model_name="Fare")
FareBreakDown = get_model(app_label="fare_enquiry", model_name="FareBreakDown")
Train = get_model(app_label="trains", model_name="Train")
Station = get_model(app_label="stations", model_name="Station")


class FareEnquirySerializer(DateFromToBaseSerializer):
    train = CharField(required=True)
    dt = DateField(required=True)
    from_station = CharField(required=True)
    to_station = CharField(required=True)
    train_cls = ChoiceField(required=True, choices=JourneyClass.get_choice())
    quota = ChoiceField(required=True, choices=TrainQuota.get_choice())

    def validate_dt(self, value):
        value = super().validate_dt(value)
        return value.strftime("%d-%m-%Y")

    def validate_train(self, value):
        if len(value) != 5:
            raise ValidationError("Train number must be 5 digits")
        try:
            train = Train.objects.get(number=value)
            return train.name_number_format
        except Train.DoesNotExist:
            raise ValidationError("Train number is invalid")


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
