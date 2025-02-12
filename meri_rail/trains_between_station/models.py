from django.db.models import (
    CASCADE,
    ForeignKey,
    TimeField,
    CharField,
    BooleanField,
    Model,
)
from django_extensions.db.models import TimeStampedModel
from trains_between_station.constants import (
    ModelVebose,
    TRAIN_BETWEEN_STATION,
    TRAINS_LIST,
)
from utils.constants import TrainType, JourneyClass


class TrainBetweenStation(TimeStampedModel):
    from_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="train_between_station_from"
    )
    to_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="train_between_station_to"
    )

    class Meta:
        verbose_name = ModelVebose.TRAIN_BETWEEN_STATION
        verbose_name_plural = ModelVebose.TRAIN_BETWEEN_STATION
        unique_together = ("from_station", "to_station")

    def __str__(self):
        return TRAIN_BETWEEN_STATION % (
            self.from_station,
            self.to_station,
        )


class TrainsList(Model):
    train = ForeignKey(
        "trains.Train",
        on_delete=CASCADE,
        related_name="trains_between_station_train_list",
    )
    train_between_station = ForeignKey(
        TrainBetweenStation, on_delete=CASCADE, related_name="trains_list"
    )
    arrival_time = TimeField()
    departure_time = TimeField()
    distance = CharField(max_length=8)
    duration = CharField(max_length=8)
    train_type = CharField(max_length=16, choices=TrainType.get_choice())
    on_monday = BooleanField(default=False)
    on_tuesday = BooleanField(default=False)
    on_wednesday = BooleanField(default=False)
    on_thursday = BooleanField(default=False)
    on_friday = BooleanField(default=False)
    on_saturday = BooleanField(default=False)
    on_sunday = BooleanField(default=False)

    class Meta:
        verbose_name = ModelVebose.TRAINS_LIST
        verbose_name_plural = ModelVebose.TRAINS_LIST
        unique_together = ("train", "train_between_station")

    def __str__(self):
        return TRAINS_LIST % (self.train, self.train_between_station)


class TrainAvailableClass(Model):
    train = ForeignKey(
        "trains.Train", on_delete=CASCADE, related_name="train_available_class"
    )
    journey_class = CharField(max_length=16, choices=JourneyClass.get_choice())
