import json
from utils.utils import get_model
from django.core.management import BaseCommand
from time import time
from meri_rail.constants import Fixtures, ManagementHelp, Messages


Train = get_model(app_label="trains", model_name="Train")


def load_data(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


class Command(BaseCommand):
    help = ManagementHelp.DUMP_TRAIN_FIXTURE

    def handle(self, *args, **options):
        start_from = time()
        trains_raw = load_data(Fixtures.TRAIN_FIXTURE)
        train_bulk = []
        for train in trains_raw:
            train_data = train.split(" - ")
            train_bulk.append(Train(**{"number": train_data[0], "name": train_data[1]}))
        Train.objects.bulk_create(train_bulk, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(Messages.INVALID_STATIONS_DUMPED % (time() - start_from))
        )
