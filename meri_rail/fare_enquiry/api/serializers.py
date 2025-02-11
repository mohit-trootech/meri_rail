from utils.utils import get_model
from utils.serializers import DynamicModelSerializer
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer
from rest_framework.serializers import (
    Serializer,
    DateField,
    CharField,
    ChoiceField,
    ValidationError,
)
from utils.constants import TrainQuota, JourneyClass
from django.utils.timezone import now

Fare = get_model(app_label="fare_enquiry", model_name="Fare")
FareBreakDown = get_model(app_label="fare_enquiry", model_name="FareBreakDown")
Train = get_model(app_label="trains", model_name="Train")
Station = get_model(app_label="stations", model_name="Station")


class FareEnquirySerializer(Serializer):
    train = CharField(required=True)
    date = DateField(required=True)
    from_station = CharField(required=True)
    to_station = CharField(required=True)
    train_cls = ChoiceField(required=True, choices=JourneyClass.get_choice())
    quota = ChoiceField(required=True, choices=TrainQuota.get_choice())

    def validate_train(self, value):
        if len(value) != 5:
            raise ValidationError("Train number must be 5 digits")
        try:
            train = Train.objects.get(number=value)
            return train.name_number_format
        except Train.DoesNotExist:
            raise ValidationError("Train number is invalid")

    def validate_from_station(self, value):
        if 0 > len(value) > 5:
            raise ValidationError("From station code must be 1-4 digits long")
        try:
            station = Station.objects.get(code=value)
            return station.name_code_format
        except Station.DoesNotExist:
            raise ValidationError("From station code is invalid")

    def validate_to_station(self, value):
        if 0 > len(value) > 5:
            raise ValidationError("From station code must be 1-4 digits long")
        try:
            station = Station.objects.get(code=value)
            return station.name_code_format
        except Station.DoesNotExist:
            raise ValidationError("To station code is invalid")

    def validate_date(self, value):
        """validate date is gte today & return in format dd-mm-yyyy"""
        if value < now().date():
            raise ValidationError("Date must be greater than or equal to today")
        return value.strftime("%d-%m-%Y")


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
