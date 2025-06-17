from utils.utils import get_model
from rest_framework.serializers import ValidationError, SerializerMethodField
from utils.constants import ValidationErrorConstants, AppLabelsModel
from trains.api.serializers import TrainDetailSerializer
from utils.serializers import DateFromToBaseSerializer

Station = get_model(**AppLabelsModel.STATION)


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
    trains = TrainDetailSerializer(many=True)
    arrival_departure_times = SerializerMethodField()

    def get_arrival_departure_times(self, obj):
        times = []
        from_station_code = obj["from_station"]
        to_station_code = obj["to_station"]

        for detail in obj["trains"]:
            route_from = detail.train.route.filter(
                station__code=from_station_code
            ).first()
            route_to = detail.train.route.filter(station__code=to_station_code).first()
            times.append(
                {
                    "train": detail.train.number,
                    "arrival": route_from.arrival if route_from else None,
                    "departure": route_to.departure if route_to else None,
                }
            )
        return times
