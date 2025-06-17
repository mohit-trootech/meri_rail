from factory.django import DjangoModelFactory
from factory.faker import Faker
from utils.constants import AppLabelsModel
from utils.utils import get_model

Station = get_model(**AppLabelsModel.STATION)


class StationFactory(DjangoModelFactory):
    class Meta:
        model = Station

    name = Faker("name")
    code = Faker("lexify", text="???".upper())
    latitude = Faker("latitude")
    longitude = Faker("longitude")
    name_hi = Faker("name")
    address = Faker("address")
