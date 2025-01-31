import json
from cities_light.models import City, Region, Country
from utils.utils import get_model
from django.core.management import BaseCommand
from django.conf import settings
from os.path import join
from time import time

country = Country.objects.get(name="India")

Station = get_model(app_label="stations", model_name="Station")
Utterance = get_model(app_label="stations", model_name="Utterance")
INVALID_FIXTURE_REGION = join(
    settings.BASE_DIR, "fixtures/stations/invalid_region.json"
)
INVALID_FIXTURE_CITY = join(settings.BASE_DIR, "fixtures/stations/invalid_city.json")


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


def temporary_station_instance(station: json):
    """creates & return temporary station instance"""
    station, created = Station.objects.get_or_create(
        name=station.get("name"),
        code=station.get("code"),
        name_hi=station.get("name_hi"),
        latitude=station.get("latitude"),
        longitude=station.get("longitude"),
        address=station.get("address"),
        trains_count=station.get("trains_count"),
    )
    if not created:
        return None
    return station


class Command(BaseCommand):
    help = "Load station data from JSON file"

    def handle(self, *args, **options):
        start_from = time()
        invalid_cities_raw = load_data(INVALID_FIXTURE_CITY)
        invalid_region_raw = load_data(INVALID_FIXTURE_REGION)
        stations = combine_raw_data(invalid_cities_raw, invalid_region_raw)
        stations_bulk = []
        for record in stations.values():
            station = temporary_station_instance(record)
            if station:
                stations_bulk.append(station)
        stations_bulk_created = Station.objects.bulk_create(
            stations_bulk, ignore_conflicts=True
        )
        for station in stations_bulk_created:
            record = stations[station.code]
            for utterance in record.get("utterances"):
                if utterance:
                    Utterance.objects.get_or_create(name=utterance, station=station)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully loaded station data, took {time() - start_from:.6f}"
            )
        )
