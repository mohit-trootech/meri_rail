from django.db.models import Model, ForeignKey, CharField, CASCADE


class Fare(Model):
    train = ForeignKey("trains.Train", on_delete=CASCADE)
    from_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="fares_from_stations"
    )
    to_station = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="fares_to_stations"
    )
    distance = CharField(max_length=16)
    total_fare = CharField(max_length=16)
    quota = CharField(max_length=16)
    train_cls = CharField(max_length=8)

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
    fare = ForeignKey(Fare, on_delete=CASCADE)
    base_fare = CharField(max_length=16)
    reservation_charge = CharField(max_length=16)
    superfast_charge = CharField(max_length=16)
    total_concession = CharField(max_length=16)
    tatkal_fare = CharField(max_length=16)
    gst_charge = CharField(max_length=16)
    other_charge = CharField(max_length=16)
    catering_charge = CharField(max_length=16)
    dynamic_fare = CharField(max_length=16)
