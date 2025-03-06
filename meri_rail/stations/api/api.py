from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from stations.api.serializers import StationSerializer
from utils.utils import get_model
from stations.constants import STATION_CACHE_KEY
from django.core.cache import cache
from rest_framework.response import Response
from http import HTTPStatus
from utils.constants import AppLabelsModel, LookUps, CacheTimeout

Station = get_model(**AppLabelsModel.STATION)


class StationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = "code__iexact"
    lookup_url_kwarg = LookUps.STATION_CODE
    search_fields = ("name", "code")
    ordering_fields = ("name", "code")
    ordering = ("name",)

    def retrieve(self, request, *args, **kwargs):
        if LookUps.STATION_CODE in kwargs:
            cache_data = cache.get(
                STATION_CACHE_KEY % kwargs[LookUps.STATION_CODE].upper()
            )
            if cache_data:
                return Response(cache_data, status=HTTPStatus.OK)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(
            STATION_CACHE_KEY % kwargs[LookUps.STATION_CODE].upper(),
            response.data,
            CacheTimeout.ONE_DAY,
        )
        return response
