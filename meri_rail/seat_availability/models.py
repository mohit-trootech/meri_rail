from django.db.models import ForeignKey, DateField, CharField, CASCADE
from django_extensions.db.models import TimeStampedModel
from seat_availability.constants import ModelVerbose, SEAT_AVAILABILITY
from utils.constants import JourneyClass, TrainQuota


class SeatAvailability(TimeStampedModel):
    train = ForeignKey(
        "trains.Train", on_delete=CASCADE, related_name="seats_availability"
    )
    from_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="from_seats_availability"
    )
    to_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="to_seats_availability"
    )
    dt = DateField(verbose_name=ModelVerbose.DATE)
    available = CharField(max_length=64)
    quota = CharField(max_length=64, choices=TrainQuota.get_choice())
    train_cls = CharField(max_length=64, choices=JourneyClass.get_choice())

    class Meta:
        verbose_name = ModelVerbose.SEAT_AVAILABILITY
        verbose_name_plural = ModelVerbose.SEATS_AVAILABILITY
        unique_together = ("train", "dt", "quota", "train_cls")

    def __str__(self):
        return SEAT_AVAILABILITY % (self.train, self.dt)
