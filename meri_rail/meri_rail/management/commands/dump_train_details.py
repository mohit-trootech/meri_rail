from utils.utils import get_model
from django.core.management import BaseCommand
from time import time
from json import load
from ast import literal_eval
from meri_rail.constants import Fixtures, ManagementHelp, Messages

Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")
Schedule = get_model(app_label="trains", model_name="Schedule")
Route = get_model(app_label="trains", model_name="Route")
Station = get_model(app_label="stations", model_name="Station")


class Command(BaseCommand):
    help = ManagementHelp.DUMP_TRAIN_FIXTURE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trains = Train.objects.all()
        if not self.trains:
            return self.stdout.write(self.style.WARNING("No self.trains found"))
        self.valid_trains = []
        self.valid_schedules = []
        self.valid_routes = []

    def handle(self, *args, **options):
        start_from = time()
        for train in self.trains:
            try:
                TrainDetail.objects.get(train=train)
            except TrainDetail.DoesNotExist:
                try:
                    with open(Fixtures.TRAIN_DETAILS_FIXTURE % train.number, "r") as fp:
                        data = load(fp)
                    try:
                        station_list = data["stationList"]
                        station_from = Station.objects.get(
                            code=station_list[0]["stationCode"]
                        )
                        station_to = Station.objects.get(
                            code=station_list[-1]["stationCode"]
                        )
                        self.valid_trains.append(
                            TrainDetail(
                                train=train,
                                station_from=station_from,
                                station_to=station_to,
                                distance=station_list[-1]["distance"],
                            )
                        )
                        self.valid_schedules.append(
                            Schedule(
                                train=train,
                                monday=data["trainRunsOnMon"],
                                tuesday=data["trainRunsOnTue"],
                                wednesday=data["trainRunsOnWed"],
                                thursday=data["trainRunsOnThu"],
                                friday=data["trainRunsOnFri"],
                                saturday=data["trainRunsOnSat"],
                                sunday=data["trainRunsOnSun"],
                            )
                        )
                        for item in data["stationList"]:
                            {
                                "stationCode": "MJ",
                                "stationName": "MARWAR JN",
                                "arrivalTime": "00:00",
                                "departureTime": "09:45",
                                "routeNumber": "0",
                                "haltTime": "--",
                                "distance": "0.0",
                                "dayCount": "1",
                                "stnSerialNumber": "1",
                            }
                            station = Station.objects.get(code=item["stationCode"])
                            route = Route(
                                train=train,
                                station=station,
                                route_number=item["routeNumber"],
                                day_count=literal_eval(item["dayCount"]),
                                platform=literal_eval(item["stnSerialNumber"]),
                            )
                            if item["haltTime"] == "--":
                                if item["arrivalTime"] == "00:00":
                                    route.halt = "src"
                                    route.departure = item["departureTime"]
                                elif item["departureTime"] == "00:00":
                                    route.arrival = item["arrivalTime"]
                                    route.halt = "dest"
                            else:
                                route.arrival = item["arrivalTime"]
                                route.departure = item["departureTime"]
                                route.halt = item["haltTime"]
                            self.valid_routes.append(route)
                    except Station.DoesNotExist:
                        continue
                except FileNotFoundError:
                    continue
        TrainDetail.objects.bulk_create(self.valid_trains, ignore_conflicts=True)
        Route.objects.bulk_create(self.valid_routes, ignore_conflicts=True)
        Schedule.objects.bulk_create(self.valid_schedules, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(Messages.TRAINS_DETAILS_DUMPED % (time() - start_from))
        )
