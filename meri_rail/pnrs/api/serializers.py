from rest_framework import serializers
from utils.serializers import DynamicModelSerializer
from utils.utils import get_model
from pnrs.utils.constants import ValidationErrors

Pnr = get_model(app_label="pnrs", model_name="Pnr")
Passengers = get_model(app_label="pnrs", model_name="Passengers")


class PnrNumberSerializer(DynamicModelSerializer):
    class Meta:
        model = Pnr
        fields = ("pnr",)

    def validate_pnr(self, value):
        """Validate Pnr Number"""
        if len(str(value)) != 10:
            raise serializers.ValidationError(ValidationErrors.INVALID_PNR_NUMBER)
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


class PnrDetailSerializer(PnrNumberSerializer):
    passengers = PassengersSerializer(many=True, read_only=True)

    class Meta(PnrNumberSerializer.Meta):
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
