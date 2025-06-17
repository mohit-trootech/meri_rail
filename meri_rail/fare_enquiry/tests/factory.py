from factory.django import DjangoModelFactory
from utils.utils import get_model
from utils.constants import AppLabelsModel

Fare = get_model(**AppLabelsModel.FARE)


class FareFactory(DjangoModelFactory):
    class Meta:
        model = Fare
