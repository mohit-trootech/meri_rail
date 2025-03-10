import json
from cities_light.models import City, Region, Country
from utils.utils import get_model
from django.core.management import BaseCommand
from time import time
from meri_rail.constants import Fixtures, ManagementHelp, Messages

country = Country.objects.get(name="India")

Station = get_model(app_label="stations", model_name="Station")
Utterance = get_model(app_label="stations", model_name="Utterance")


def load_data(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


def combine_raw_data(stations: json, popular: json) -> dict:
    """
    Combine both json files with drop duplicate data.
    :param stations: json
    :param popular: json
    """
    data = {}
    codes = set()
    for station in stations:
        codes.add(station.get("code"))
    for station in stations:
        data[station["code"]] = station
    for popular_station in popular:
        data[station["code"]] = popular_station
    return data


def create_region_instance(station: json):
    """creates & return region instance"""
    try:
        region, created = Region.objects.get_or_create(
            name=station.get("state"), name_ascii=station.get("state"), country=country
        )
    except Region.MultipleObjectsReturned:
        region = Region.objects.filter(name__contains=station.get("state"))[0]
    city = create_city_instance(station, region)
    return region, city


def create_city_instance(station: json, region: Region):
    """creates & return city instance"""
    try:
        city, created = City.objects.get_or_create(
            name=station.get("district"),
            name_ascii=station.get("district"),
            region=region,
            country=country,
        )
    except City.MultipleObjectsReturned:
        city = City.objects.filter(name__contains=station.get("district"))[0]
    return city


def temporary_station_instance(station: json, region: Region, city: City):
    """creates & return temporary station instance"""
    return Station(
        name=station.get("name"),
        code=station.get("code"),
        name_hi=station.get("name_hi"),
        district=city,
        state=region,
        latitude=station.get("latitude"),
        longitude=station.get("longitude"),
        address=station.get("address"),
        trains_count=station.get("trains_count"),
    )


class Command(BaseCommand):
    help = ManagementHelp.DUMP_STATION_FIXTURE

    def handle(self, *args, **options):
        start_from = time()
        stations_raw = load_data(Fixtures.STATION_FIXTURE)
        popular_raw = load_data(Fixtures.POPULAR_FIXTURE)
        stations = combine_raw_data(stations_raw, popular_raw)
        stations_bulk = []
        city_error = []
        region_error = []
        for record in stations.values():
            try:
                city = City.objects.get(name_ascii__contains=record.get("district"))
                region = Region.objects.get(name_ascii__contains=record.get("state"))
                station_obj = temporary_station_instance(record, region, city)
                if station_obj:
                    stations_bulk.append(station_obj)
            except City.MultipleObjectsReturned:
                if record["district"] == "":
                    pass
                if record["state"] == "":
                    pass
                try:
                    region = Region.objects.get(name_ascii__contains=record["state"])
                    city = City.objects.get(
                        name_ascii__contains=record["district"], region=region
                    )
                    stations_bulk.append(
                        temporary_station_instance(record, region, city)
                    )
                except (City.DoesNotExist, City.MultipleObjectsReturned):
                    city_error.append(record)
                except (Region.DoesNotExist, Region.MultipleObjectsReturned):
                    region_error.append(record)
            except Region.MultipleObjectsReturned:
                if record.get("state") == "":
                    region_error.append(record)
                if record.get("district") == "":
                    region_error.append(record)
                city = City.objects.get(name_ascii__contains=record.get("district"))
                region = Region.objects.filter(name__contains=record.get("state"))[0]
                stations_bulk.append(temporary_station_instance(record, region, city))
            except (Region.DoesNotExist, City.DoesNotExist):
                region, city = create_region_instance(record)
                station_obj = temporary_station_instance(record, region, city)
                if station_obj:
                    stations_bulk.append(station_obj)
        stations_bulk_created = Station.objects.bulk_create(
            stations_bulk, ignore_conflicts=True
        )
        for station in stations_bulk_created:
            record = stations[station.code]
            if record.get("utterances"):
                for utterance in record.get("utterances"):
                    Utterance.objects.get_or_create(name=utterance, station=station)
        if city_error:
            with open(Fixtures.INVALID_FIXTURE_CITY, "w") as file:
                json.dump(city_error, file, indent=4)
        if region_error:
            with open(Fixtures.INVALID_FIXTURE_REGION, "w") as file:
                json.dump(region_error, file, indent=4)
        self.stdout.write(
            self.style.SUCCESS(Messages.STATIONS_DUMPED % (time() - start_from))
        )
