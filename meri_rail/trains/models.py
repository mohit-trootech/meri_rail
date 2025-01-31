from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    CASCADE,
)


class Train(Model):
    number = CharField(max_length=5, unique=True)
    name = CharField(max_length=100)

    class Meta:
        ordering = ["number"]
        verbose_name = "Train"
        verbose_name_plural = "Trains"


class TrainDetails(Model):
    train = ForeignKey("trains.Train", on_delete=CASCADE, related_name="train_details")
