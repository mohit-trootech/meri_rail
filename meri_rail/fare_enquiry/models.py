from django.db.models import Model, OneToOneField, CharField, CASCADE, ForeignKey
from utils.constants import TrainQuota, JourneyClass
from django_extensions.db.models import TimeStampedModel


class Fare(TimeStampedModel):
    train = ForeignKey("trains.Train", on_delete=CASCADE)
    from_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="fares_from_stations"
    )
    to_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="fares_to_stations"
    )
    distance = CharField(max_length=16)
    total_fare = CharField(max_length=16)
    quota = CharField(
        max_length=16, choices=TrainQuota.get_choice(), default=TrainQuota.GN
    )
    train_cls = CharField(
        max_length=8, choices=JourneyClass.get_choice(), default=JourneyClass.SL
    )

    class Meta:
        verbose_name = "Fare"
        verbose_name_plural = "Fare"
        unique_together = ("train", "from_station", "to_station", "quota", "train_cls")

    def __str__(self):
        return "%s (%s - %s) %s %s" % (
            self.train,
            self.from_station.code,
            self.to_station.code,
            self.quota,
            self.train_cls,
        )


class FareBreakDown(Model):
    fare = OneToOneField(Fare, on_delete=CASCADE, related_name="breakdown")
    base_fare = CharField(max_length=16)
    reservation_charge = CharField(max_length=16, blank=True, null=True)
    superfast_charge = CharField(max_length=16, blank=True, null=True)
    total_concession = CharField(max_length=16, blank=True, null=True)
    tatkal_fare = CharField(max_length=16, blank=True, null=True)
    gst_charge = CharField(max_length=16, blank=True, null=True)
    other_charge = CharField(max_length=16, blank=True, null=True)
    catering_charge = CharField(max_length=16, blank=True, null=True)
    dynamic_fare = CharField(max_length=16, blank=True, null=True)
