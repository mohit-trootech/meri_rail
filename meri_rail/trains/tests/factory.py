from factory.django import DjangoModelFactory
from factory import SubFactory
from factory.faker import Faker
from utils.constants import AppLabelsModel
from utils.utils import get_model


class TrainFactory(DjangoModelFactory):
    class Meta:
        model = get_model(AppLabelsModel.TRAIN)

    number = Faker("numerify", text="#####")
    name = Faker("name")


class TrainDetailFactory(DjangoModelFactory):
    class Meta:
        model = get_model(AppLabelsModel.TRAIN_DETAIL)

    train = SubFactory(TrainFactory)
    station_from = SubFactory("stations.tests.factory.StationFactory")
    station_to = SubFactory("stations.tests.factory.StationFactory")
    distance = Faker("numerify", text="###")


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = get_model(AppLabelsModel.SCHEDULE)

    train = SubFactory(TrainFactory)
    monday = "Y"
    tuesday = "Y"
    wednesday = "Y"
    thursday = "Y"
    friday = "Y"
    saturday = "Y"
    sunday = "Y"


class RouteFactory(DjangoModelFactory):
    class Meta:
        model = get_model(AppLabelsModel.ROUTE)

    train = SubFactory(TrainFactory)
    station = SubFactory("stations.tests.factory.StationFactory")
    route_number = Faker("numerify", text="###")
    halt = Faker("numerify", text="##")
    day_count = Faker("random_int", min=1, max=7)
    platform = Faker("random_int", min=1, max=10)
    arrival = Faker("time_object")
    departure = Faker("time_object")
