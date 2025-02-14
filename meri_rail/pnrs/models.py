from django.db.models import (
    Model,
    CharField,
    DateField,
    IntegerField,
    BigIntegerField,
    CASCADE,
    ForeignKey,
    ManyToManyField,
)
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from utils.constants import TrainQuota


class Pnr(TimeStampedModel):
    users = ManyToManyField("users.User", related_name="pnrs")
    pnr = BigIntegerField(unique=True)
    date_of_journey = DateField()
    train = ForeignKey("trains.Train", on_delete=CASCADE, related_name="pnrs")
    source = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="source_pnrs"
    )
    destination = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="destination_pnrs"
    )
    boarding = ForeignKey(
        "stations.Station", on_delete=CASCADE, related_name="boarding_pnrs"
    )
    journey_class = CharField(max_length=8, null=True, blank=True)
    number_of_passengers = IntegerField(null=True, blank=True)
    chart_status = CharField(max_length=64, null=True, blank=True)
    cancel_status = CharField(max_length=64, null=True, blank=True)
    booking_fare = IntegerField(null=True, blank=True)
    ticket_fare = IntegerField(null=True, blank=True)
    quota = CharField(
        max_length=16, choices=TrainQuota.get_choice(), null=True, blank=True
    )
    vikalp_otp = CharField(max_length=8, null=True, blank=True)
    booking_date = DateField(null=True, blank=True)
    mobile_number = PhoneNumberField(region="IN", null=True, blank=True)
    distance = IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Pnr"
        verbose_name_plural = "Pnr"

    def add_user_to_pnr(self, user):
        """Adds the given user to the pnr's users field."""
        self.users.add(user.pk)

    def __str__(self):
        return str(self.pnr)


class Passengers(Model):
    pnr = ForeignKey("pnrs.Pnr", on_delete=CASCADE, related_name="passengers")
    serial_number = IntegerField()
    quota = CharField(
        max_length=16, choices=TrainQuota.get_choice(), null=True, blank=True
    )
    nationality = CharField(max_length=8, null=True, blank=True)
    waitlist_type = CharField(max_length=16, null=True, blank=True)
    booking_status = CharField(max_length=16, null=True, blank=True)
    booking_coach = CharField(max_length=16, null=True, blank=True)
    booking_berth = CharField(max_length=16, null=True, blank=True)
    booking_details = CharField(max_length=32, null=True, blank=True)
    current_status = CharField(max_length=16, null=True, blank=True)
    current_coach = CharField(max_length=16, null=True, blank=True)
    current_berth = CharField(max_length=16, null=True, blank=True)
    current_details = CharField(max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "Passengers"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return str(self.serial_number)
