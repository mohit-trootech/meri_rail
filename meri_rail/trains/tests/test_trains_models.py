from trains.tests.factory import (
    TrainFactory,
    TrainDetailFactory,
    RouteFactory,
    ScheduleFactory,
)
from utils.tests.base import TestModel
from utils.utils import get_model
from utils.constants import AppLabelsModel
from trains.constants import TRAIN_STR


class TestTrainModel(TestModel):
    model = get_model(**AppLabelsModel.TRAIN)
    factory_class = TrainFactory

    def test_train_model(self):
        train = self.factory_create()
        self.assertTrue(isinstance(train, self.model))
        self.assertEqual(str(train), TRAIN_STR % (train.number, train.name))
        self.assertEqual(train, self.model.objects.get(number=train.number))


class TestTrainDetailModel(TestModel):
    model = get_model(**AppLabelsModel.TRAIN_DETAIL)
    factory_class = TrainDetailFactory

    def test_train_detail_str(self):
        train_detail = self.factory_class()
        self.assertTrue(isinstance(train_detail, self.model))
        self.assertEqual(train_detail, self.model.objects.get(train=train_detail.train))


class TestScheduleModel(TestModel):
    model = get_model(**AppLabelsModel.SCHEDULE)
    factory_class = ScheduleFactory

    def test_schedule_str(self):
        schedule = self.factory_create()
        self.assertTrue(
            isinstance(schedule, self.model),
        )


class TestRouteModel(TestModel):
    model = get_model(**AppLabelsModel.ROUTE)
    factory_class = RouteFactory

    def test_route_str(self):
        route = self.factory_create()
        self.assertTrue(isinstance(route, self.model))
