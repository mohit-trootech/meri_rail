from utils.serializers import DynamicModelSerializer
from utils.utils import get_model
from cities_light.models import City, Region, Country
from utils.constants import AppLabelsModel

Station = get_model(**AppLabelsModel.STATION)
Utterance = get_model(**AppLabelsModel.UTTERANCES)


class CitiesLightBaseSerializer(DynamicModelSerializer):
    class Meta:
        fields = ["name", "name_ascii", "geoname_id"]


class CountrySerializer(CitiesLightBaseSerializer):
    class Meta(CitiesLightBaseSerializer.Meta):
        model = Country
        fields = CitiesLightBaseSerializer.Meta.fields + ["code2"]


class CitySerializer(CitiesLightBaseSerializer):
    class Meta(CitiesLightBaseSerializer.Meta):
        model = City
        fields = CitiesLightBaseSerializer.Meta.fields + [
            "latitude",
            "longitude",
            "population",
            "feature_code",
            "timezone",
        ]


class RegionSerializer(CitiesLightBaseSerializer):
    country = CountrySerializer(many=False, read_only=True)

    class Meta(CitiesLightBaseSerializer.Meta):
        model = Region
        fields = CitiesLightBaseSerializer.Meta.fields + ["country"]


class UtteranceSerializer(DynamicModelSerializer):
    class Meta:
        model = Utterance
        fields = ("name",)


class StationSerializer(DynamicModelSerializer):
    district = CitySerializer(many=False, read_only=True)
    state = RegionSerializer(many=False, read_only=True)
    utterances = UtteranceSerializer(many=True, read_only=True)

    class Meta:
        model = Station
        fields = (
            "name",
            "code",
            "name_hi",
            "district",
            "state",
            "latitude",
            "longitude",
            "address",
            "trains_count",
            "utterances",
        )
