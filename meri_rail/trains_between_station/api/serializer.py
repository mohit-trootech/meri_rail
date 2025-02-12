from utils.utils import get_model
from utils.serializers import DynamicModelSerializer
from trains.api.serializers import TrainSerializer
from stations.api.serializers import StationSerializer
from utils.serializers import DateFromToBaseSerializer
from django.db import IntegrityError, transaction

TrainsList = get_model(app_label="trains_between_station", model_name="TrainsList")
TrainBetweenStation = get_model(
    app_label="trains_between_station", model_name="TrainBetweenStation"
)
Station = get_model(app_label="stations", model_name="Station")


class TbisSerializer(DateFromToBaseSerializer):
    pass


class TrainListSerializer(DynamicModelSerializer):
    train = TrainSerializer(many=False, read_only=True)

    class Meta:
        model = TrainsList
        fields = (
            "train",
            "arrival_time",
            "departure_time",
            "distance",
            "duration",
            "train_type",
            "on_monday",
            "on_tuesday",
            "on_wednesday",
            "on_thursday",
            "on_friday",
            "on_saturday",
            "on_sunday",
        )


class TrainBetweenStationSerializer(DynamicModelSerializer):
    from_station = StationSerializer(many=False, read_only=True)
    to_station = StationSerializer(many=False, read_only=True)
    trains_list = TrainListSerializer(many=True, read_only=True)

    class Meta:
        model = TrainBetweenStation
        fields = ("from_station", "to_station", "trains_list")

    def create(self, validated_data):
        """Create TrainBetweenStation and related TrainsList instances with transaction management."""
        try:
            with transaction.atomic():
                for trains_list in self.initial_data:
                    from_station_id = trains_list.pop("from_station_id")
                    to_station_id = trains_list.pop("to_station_id")

                    instance, created = TrainBetweenStation.objects.get_or_create(
                        from_station=from_station_id,
                        to_station=to_station_id,
                    )
                    trains_list.update({"train_between_station_id": instance.id})

                    train_list_instance, created = TrainsList.objects.get_or_create(
                        **trains_list
                    )
                    instance.trains_list.add(train_list_instance)
                    instance.save()
                return instance
        except IntegrityError:
            pass
        except Exception:
            pass
