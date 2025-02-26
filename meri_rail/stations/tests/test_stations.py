from stations.tests.factory import StationFactory
from utils.tests.base import TestModel, TestClientCRUD
from utils.utils import get_model
from utils.constants import AppLabelsModel
from stations.api.serializers import StationSerializer

Station = get_model(**AppLabelsModel.STATION)


class TestStationModel(TestModel):
    model = Station
    factory_class = StationFactory

    def test_station_creation(self):
        instance = self.factory_create()
        self.assertIsNotNone(instance)
        self.assertIsNotNone(instance.name)
        self.assertIsNotNone(instance.name_hi)
        self.assertIsNotNone(instance.code)
        self.assertIsNotNone(instance.address)
        self.assertIsNotNone(instance.latitude)
        self.assertIsNotNone(instance.longitude)
        self.assertTrue(isinstance(instance, self.model))


class TestStationApi(TestClientCRUD):
    model = Station
    factory_class = StationFactory
    list_url = "/api/stations/"
    detail_url = "/api/stations/{}/"
    serializer_class = StationSerializer

    def test_list_stations(self):
        instances = self.factory_create_many()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), len(instances))

    def test_create_station(self):
        data = {
            "name": "Test Station",
            "code": "TST",
            "latitude": 12.345,
            "longitude": 67.890,
            "name_hi": "टेस्ट स्टेशन",
            "address": "Test Address",
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, 405)

    def test_detail_station(self):
        instance = self.factory_create()
        response = self.client.get(self.detail_url.format(instance.code))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], instance.code)
        self.assertEqual(response.data["name"], instance.name)
        self.assertEqual(response.data["name_hi"], instance.name_hi)
        self.assertEqual(response.data["latitude"], str(instance.latitude))
        self.assertEqual(response.data["longitude"], str(instance.longitude))
        self.assertEqual(response.data["address"], instance.address)
        self.serializer_validation(response=response, instance=instance)

    def test_update_station(self):
        data = {
            "name": "Updated Station",
        }
        instance = self.factory_create()
        response = self.client.patch(self.detail_url.format(instance.code), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], data["name"])
        instance.refresh_from_db()
        self.assertEqual(instance.name, data["name"])
        self.serializer_validation(response=response, instance=instance)

    def test_delete_station(self):
        instance = self.factory_create()
        response = self.client.delete(self.detail_url.format(instance.code))
        self.assertEqual(response.status_code, 405)
