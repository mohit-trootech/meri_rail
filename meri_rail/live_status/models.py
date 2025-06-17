from django.db import models
from django_extensions.db.models import TimeStampedModel
from live_status.constants import ModelStr, ModelVerbose


class LiveHistory(TimeStampedModel):
    train = models.ForeignKey(
        "trains.Train", on_delete=models.CASCADE, related_name="live_history"
    )
    station = models.ForeignKey(
        "stations.Station",
        on_delete=models.CASCADE,
        related_name="live_history",
    )
    arrival = models.DateTimeField()
    departure = models.DateTimeField()
    date = models.DateField()
    delay = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        unique_together = ("train", "station", "date")
        verbose_name = ModelStr.LIVE_HISTORY
        verbose_name_plural = ModelVerbose.LIVE_HISTORY
        ordering = ["-date"]

    def __str__(self):
        return ModelStr.LIVE_HISTORY % (self.train, self.station, self.date)


class LiveStatus(models.Model):
    date = models.DateField()
    train = models.ForeignKey(
        "trains.Train", on_delete=models.CASCADE, related_name="live_statuses"
    )
    departed_station = models.ForeignKey(
        "stations.Station",
        on_delete=models.CASCADE,
        related_name="live_status_departed",
    )
    upcoming_station = models.ForeignKey(
        "stations.Station",
        on_delete=models.CASCADE,
        related_name="live_status_upcoming",
    )
    departed_time = models.DateTimeField()
    delay = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        unique_together = ("train", "date")
        verbose_name = ModelStr.LIVE_STATUS
        verbose_name_plural = ModelVerbose.LIVE_STATUS
        ordering = ["-date"]

    def __str__(self):
        return ModelStr.LIVE_STATUS % (self.train, self.date)
