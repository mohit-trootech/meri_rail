from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from stations.api.serializers import StationSerializer
from utils.utils import get_model
from stations.constants import STATION_CACHE_KEY
from django.core.cache import cache
from rest_framework.response import Response
from http import HTTPStatus

Station = get_model(app_label="stations", model_name="Station")


class StationViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = "code__iexact"
    lookup_url_kwarg = "code"
    search_fields = ("name", "code")
    ordering_fields = ("name", "code")
    ordering = ("name",)

    def retrieve(self, request, *args, **kwargs):
        if "code" in kwargs:
            cache_data = cache.get(STATION_CACHE_KEY % kwargs["code"].upper())
            if cache_data:
                return Response(cache_data, status=HTTPStatus.OK)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(
            STATION_CACHE_KEY % kwargs["code"].upper(), response.data, 60 * 60 * 24
        )
        return response
