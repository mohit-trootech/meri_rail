from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from stations.api.serializers import StationSerializer
from utils.utils import get_model

Station = get_model(app_label="stations", model_name="Station")


class StationViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = "code"
    search_fields = ("name", "code", "district__name_ascii")
