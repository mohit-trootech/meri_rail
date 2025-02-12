from rest_framework import serializers
from utils.serializers import DynamicModelSerializer
from utils.utils import get_model
from pnrs.constants import ValidationErrorsConstants
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer

Pnr = get_model(app_label="pnrs", model_name="Pnr")
Passengers = get_model(app_label="pnrs", model_name="Passengers")


class PnrNumberSerializer(serializers.Serializer):
    pnr = serializers.CharField()

    def validate_pnr(self, value):
        """Validate Pnr Number"""
        if len(value) != 10:
            raise serializers.ValidationError(
                ValidationErrorsConstants.INVALID_PNR_NUMBER
            )
        return value


class PassengersSerializer(DynamicModelSerializer):
    class Meta:
        model = Passengers
        fields = (
            "serial_number",
            "quota",
            "nationality",
            "waitlist_type",
            "booking_status",
            "booking_coach",
            "booking_berth",
            "booking_details",
            "current_status",
            "current_coach",
            "current_berth",
            "current_details",
        )


class PnrDetailSerializer(DynamicModelSerializer):
    passengers = PassengersSerializer(
        read_only=True,
        many=True,
    )
    train = TrainSerializer(read_only=True, many=False)
    source = StationSerializer(read_only=True, many=False)
    destination = StationSerializer(read_only=True, many=False)
    boarding = StationSerializer(read_only=True, many=False)

    class Meta:
        model = Pnr
        fields = (
            "pnr",
            "date_of_journey",
            "train",
            "source",
            "destination",
            "boarding",
            "journey_class",
            "number_of_passengers",
            "chart_status",
            "cancel_status",
            "booking_fare",
            "ticket_fare",
            "quota",
            "vikalp_otp",
            "booking_date",
            "mobile_number",
            "distance",
            "passengers",
        )

    def create(self, validated_data):
        passengers = validated_data.pop("passengers")
        instance = super().create(validated_data)
        for passenger in passengers:
            try:
                Passengers.objects.create(pnr=instance, **passenger)
            except Exception as err:
                instance.delete()
                raise serializers.ValidationError({"message": str(err)})
        return instance
