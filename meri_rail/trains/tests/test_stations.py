from trains.tests.factory import (
    TrainFactory,
    TrainDetailFactory,
    RouteFactory,
    ScheduleFactory,
)
from utils.tests.base import TestModel
from utils.utils import get_model
from utils.constants import AppLabelsModel


class TestTrainModel(TestModel):
    model = get_model(AppLabelsModel.TRAIN)
    factory_class = TrainFactory

    def test_train_str(self):
        train = self.factory()
        self.assertEqual(str(train), f"{train.number} {train.name}")

    def test_train_name_number_format(self):
        train = self.factory(name="New Delhi")
        self.assertEqual(train.name_number_format, f"{train.number}+New+Delhi")


class TestTrainDetailModel(TestModel):
    model = get_model(AppLabelsModel.TRAIN_DETAIL)
    factory = TrainDetailFactory

    def test_train_detail_str(self):
        train_detail = self.factory()
        self.assertEqual(
            str(train_detail),
            f"{train_detail.train.number} {train_detail.train.name}",
        )


class TestScheduleModel(TestModel):
    model = get_model(AppLabelsModel.SCHEDULE)
    factory = ScheduleFactory

    def test_schedule_str(self):
        schedule = self.factory()
        self.assertEqual(
            str(schedule), f"{schedule.train.number} {schedule.train.name}"
        )


class TestRouteModel(TestModel):
    model = get_model(AppLabelsModel.ROUTE)
    factory = RouteFactory

    def test_route_str(self):
        route = self.factory()
        self.assertEqual(str(route), f"{route.train.number} {route.train.name}")

    def test_route_runs_on_days(self):
        route = self.factory()
        self.assertEqual(len(route.runs_on_days), 7)
