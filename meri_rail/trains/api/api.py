from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from utils.utils import get_model
from trains.api.serializers import (
    TrainSerializer,
    TrainDetailSerializer,
)
from django.core.cache import cache
from http import HTTPStatus
from rest_framework.response import Response
from trains.constants import TRAIN_CACHE_KEY

Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")


class TrainViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = TrainDetail.objects.all()
    serializer_class = TrainDetailSerializer
    lookup_field = "train__number"
    ordering_fields = [
        "number",
        "name",
        "details__distance",
    ]
    search_fields = ["name", "number"]

    def get_queryset(self):
        if self.action == "list":
            return Train.objects.all()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        if "train__number" in kwargs:
            cache_data = cache.get(TRAIN_CACHE_KEY % kwargs["train__number"])
            if cache_data:
                return Response(cache_data, status=HTTPStatus.OK)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(
            TRAIN_CACHE_KEY % kwargs["train__number"], response.data, 60 * 60 * 24
        )
        return response
