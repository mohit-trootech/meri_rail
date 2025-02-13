from utils.utils import get_model
from rest_framework.serializers import ValidationError
from utils.constants import ValidationErrorConstants
from trains.api.serializers import TrainSerializer
from utils.serializers import DateFromToBaseSerializer

Station = get_model(app_label="stations", model_name="Station")
Route = get_model(app_label="trains", model_name="Route")


class TbisSerializer(DateFromToBaseSerializer):
    def validate_from_station(self, value):
        try:
            return Station.objects.get(code=value.upper()).code
        except Station.DoesNotExist:
            raise ValidationError(ValidationErrorConstants.STATION_NOT_FOUND)

    def validate_to_station(self, value):
        try:
            return Station.objects.get(code=value.upper()).code
        except Station.DoesNotExist:
            raise ValidationError(ValidationErrorConstants.STATION_NOT_FOUND)


class TrainBetweenStationSerializer(DateFromToBaseSerializer):
    trains = TrainSerializer(many=True)
