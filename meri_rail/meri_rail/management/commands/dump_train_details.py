from utils.utils import get_model
from django.core.management import BaseCommand
from time import time
from meri_rail.constants import Fixtures, ManagementHelp, Messages
from utils.selenium_service import SeleniumService

Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")


class Command(BaseCommand):
    help = ManagementHelp.DUMP_TRAIN_FIXTURE
    service_class = SeleniumService

    def handle(self, *args, **options):
        start_from = time()
        trains = Train.objects.all()
        if not trains:
            return self.stdout.write(self.style.ERROR("No trains found"))
        # trains_raw = load_data(Fixtures.TRAIN_FIXTURE + "12915.json")
        # train_bulk = []
        fake_driver = self.service_class()
        for train in trains:
            train_raw_str = train.name_number
            try:
                captcha = fake_driver.validate_captcha()
                data = fake_driver.load_train_details(
                    captcha=captcha, train=train_raw_str
                )
                if data:
                    with open(
                        Fixtures.TRAIN_DETAILS_FIXTURE + f"{train.number}.json", "w"
                    ) as file:
                        file.write(data)
                    print("Train Data Fetched ", train_raw_str)
            except Exception:
                pass
        fake_driver.driver.quit()
        # Train.objects.bulk_create(train_bulk, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(Messages.INVALID_STATIONS_DUMPED % (time() - start_from))
        )
