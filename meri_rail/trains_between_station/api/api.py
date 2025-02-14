from utils.utils import get_model
from trains_between_station.api.serializer import (
    TbisSerializer,
    TrainBetweenStationSerializer,
)
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.response import Response
from utils.tbis_queryset import find_trains_between_stations
from trains_between_station.constants import TBIS_CACHE_KEY
from django.core.cache import cache

Route = get_model(app_label="trains", model_name="Route")


class TrainBetweenStationApiView(APIView):
    def get(self, request):
        tbis_serializer = TbisSerializer(data=request.data)
        tbis_serializer.is_valid(raise_exception=True)
        cache_data = cache.get(TBIS_CACHE_KEY % tbis_serializer.validated_data)
        if cache_data:
            return Response(cache_data, status=HTTPStatus.OK)
        qs = find_trains_between_stations(
            station_from_code=tbis_serializer.validated_data["from_station"],
            station_to_code=tbis_serializer.validated_data["to_station"],
            date=tbis_serializer.validated_data["dt"],
        )
        serializer = TrainBetweenStationSerializer(
            {"trains": qs, **tbis_serializer.validated_data}
        )
        cache.set(
            TBIS_CACHE_KEY % tbis_serializer.validated_data,
            serializer.data,
            60 * 60 * 24,
        )
        return Response(serializer.data, status=HTTPStatus.OK)


train_between_station_view = TrainBetweenStationApiView.as_view()
