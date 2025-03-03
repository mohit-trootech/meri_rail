from utils.utils import get_model
from django.core.management import BaseCommand
from time import time
from json import dump, loads
from meri_rail.constants import Fixtures, ManagementHelp, Messages
from utils.selenium_service import SeleniumService

Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")
Station = get_model(app_label="stations", model_name="Station")


class Command(BaseCommand):
    help = ManagementHelp.DUMP_TRAIN_FIXTURE
    service_class = SeleniumService

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invalid_trains = []
        self.trains = Train.objects.all()
        self.manager_driver = SeleniumService()
        if not self.trains:
            return self.stdout.write(self.style.WARNING("No self.trains found"))

    def handle(self, *args, **options):
        start_from = time()
        for train in self.trains:
            try:
                TrainDetail.objects.get(train=train)
            except TrainDetail.DoesNotExist:
                try:
                    open(Fixtures.TRAIN_DETAILS_FIXTURE % train.number).close()
                except FileNotFoundError:
                    try:
                        captcha = self.manager_driver.validate_captcha()
                        data = self.manager_driver.load_train_details(
                            captcha=captcha, train=train.name_number_format
                        )
                        if "errorMessage" in data:
                            print(loads(data)["errorMessage"])
                            self.invalid_trains.append(train.number)
                            continue
                        if data:
                            with open(
                                Fixtures.TRAIN_DETAILS_FIXTURE % train.number, "w"
                            ) as file:
                                file.write(data)
                            print("Train Data Fetched ", train.name_number_format)
                    except Exception as err:
                        print(err)
                        self.invalid_trains.append(train.number)
                        continue
        self.manager_driver.driver.quit()
        if self.invalid_trains:
            with open(
                file=Fixtures.INVALID_TRAIN_FIXTURE, mode="w", encoding="utf8"
            ) as file:
                dump(self.invalid_trains, file)
        self.stdout.write(
            self.style.SUCCESS(Messages.TRAINS_DETAILS_FETCHED % (time() - start_from))
        )
