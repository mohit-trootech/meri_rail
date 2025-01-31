from django.db.models import (
    Model,
    CharField,
    DateField,
    IntegerField,
    CASCADE,
    ForeignKey,
)
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Pnr(TimeStampedModel):
    pnr = IntegerField(unique=True)
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
    journey_class = CharField(max_length=8)
    number_of_passengers = IntegerField()
    fare = IntegerField()
    chart_status = CharField(max_length=64)
    cancel_status = CharField(max_length=64)
    booking_fare = IntegerField()
    ticket_fare = IntegerField()
    quota = CharField(max_length=16)
    vikalp_otp = CharField(max_length=8)
    booking_date = DateField()
    mobile_number = PhoneNumberField(region="IN", null=True, blank=True)
    distance = IntegerField()


class Passengers(Model):
    pnr = ForeignKey("pnrs.Pnr", on_delete=CASCADE, related_name="passengers")
    serial_number = IntegerField()
    quota = CharField(max_length=16, null=True, blank=True)
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
