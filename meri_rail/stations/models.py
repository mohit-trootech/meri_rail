from django.db.models import (
    Model,
    CharField,
    IntegerField,
    TextField,
    ForeignKey,
    CASCADE,
)
from stations.constants import ModelVerbose, STATION_NAME_CODE_VALID_FORMAT
from cities_light.models import City, Region


class Station(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=8, unique=True)
    name_hi = CharField(max_length=512)
    district = ForeignKey(
        City, null=True, blank=True, on_delete=CASCADE, related_name="stations"
    )
    state = ForeignKey(
        Region, null=True, blank=True, on_delete=CASCADE, related_name="stations"
    )
    latitude = CharField(null=True, blank=True)
    longitude = CharField(null=True, blank=True)
    address = TextField(null=True, blank=True)
    trains_count = IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = ModelVerbose.STATION
        verbose_name_plural = ModelVerbose.STATIONS

    def __str__(self):
        return self.code

    @property
    def name_code_format(self):
        return STATION_NAME_CODE_VALID_FORMAT % (
            self.name.replace(" ", "+"),
            self.code,
        )


class Utterance(Model):
    name = CharField(max_length=255, unique=True)
    station = ForeignKey(
        "stations.Station",
        blank=True,
        null=True,
        related_name="utterances",
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = ModelVerbose.UTTERANCE
        verbose_name_plural = ModelVerbose.UTTERANCES
        unique_together = ("name", "station")

    def __str__(self):
        return self.name
