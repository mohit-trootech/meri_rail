from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE,
    OneToOneField,
    TimeField,
    IntegerField,
)
from trains.constants import (
    TRAIN_NAME_NUMBER_VALID_FORMAT,
    ModelVerbose,
    TRAIN_STR,
)
from utils.constants import DayFormat


class Train(Model):
    number = CharField(max_length=5, unique=True)
    name = CharField(max_length=100)

    class Meta:
        verbose_name = ModelVerbose.TRAIN
        verbose_name_plural = ModelVerbose.TRAINS

    def __str__(self):
        return TRAIN_STR % (self.number, self.name)

    @property
    def name_number_format(self):
        return TRAIN_NAME_NUMBER_VALID_FORMAT % (
            self.number,
            self.name.replace(" ", "+"),
        )


class TrainDetail(Model):
    train = OneToOneField("trains.Train", on_delete=CASCADE, related_name="details")
    station_from = ForeignKey(
        "stations.Station",
        on_delete=CASCADE,
        related_name="station_from",
        null=True,
        blank=True,
    )
    station_to = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="station_to"
    )
    distance = CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = ModelVerbose.TRAIN_DETAIL
        verbose_name_plural = ModelVerbose.TRAIN_DETAIL

    def __str__(self):
        return TRAIN_STR % (self.train.number, self.train.name)


class Schedule(Model):
    train = OneToOneField("trains.Train", on_delete=CASCADE, related_name="schedule")
    monday = CharField(max_length=10, null=True, blank=True)
    tuesday = CharField(max_length=10, null=True, blank=True)
    wednesday = CharField(max_length=10, null=True, blank=True)
    thursday = CharField(max_length=10, null=True, blank=True)
    friday = CharField(max_length=10, null=True, blank=True)
    saturday = CharField(max_length=10, null=True, blank=True)
    sunday = CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = ModelVerbose.SCHEDULE
        verbose_name_plural = ModelVerbose.SCHEDULE

    def __str__(self):
        return TRAIN_STR % (self.train.number, self.train.name)


class Route(Model):
    train = ForeignKey("trains.Train", on_delete=CASCADE, related_name="route")
    station = ForeignKey("stations.Station", on_delete=CASCADE, related_name="route")
    route_number = CharField(max_length=3)
    halt = CharField(max_length=10, null=True, blank=True)
    day_count = IntegerField(null=True, blank=True)
    platform = IntegerField(null=True, blank=True)
    arrival = TimeField(null=True, blank=True)
    departure = TimeField(null=True, blank=True)

    class Meta:
        verbose_name = ModelVerbose.ROUTE
        verbose_name_plural = ModelVerbose.ROUTE

    def __str__(self):
        return TRAIN_STR % (self.train.number, self.train.name)

    @property
    def runs_on_days(self):
        """list of weekdays train runs on"""
        week_days = []
        if self.train.schedule.monday == "Y":
            week_days.append(DayFormat.MONDAY + self.day_count - 1)
        if self.train.schedule.tuesday == "Y":
            week_days.append(DayFormat.TUESDAY + self.day_count - 1)
        if self.train.schedule.wednesday == "Y":
            week_days.append(DayFormat.WEDNESDAY + self.day_count - 1)
        if self.train.schedule.thursday == "Y":
            week_days.append(DayFormat.THURSDAY + self.day_count - 1)
        if self.train.schedule.friday == "Y":
            week_days.append(DayFormat.FRIDAY + self.day_count - 1)
        if self.train.schedule.saturday == "Y":
            week_days.append(DayFormat.SATURDAY + self.day_count - 1)
        if self.train.schedule.sunday == "Y":
            week_days.append(DayFormat.SUNDAY + self.day_count - 1)
        return week_days
