from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from utils.utils import get_model
from trains.api.serializers import (
    TrainSerializer,
    TrainDetailSerializer,
)


Train = get_model(app_label="trains", model_name="Train")
TrainDetail = get_model(app_label="trains", model_name="TrainDetail")


class TrainViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = TrainDetail.objects.all()
    serializer_class = TrainDetailSerializer
    lookup_field = "train__number"

    def get_queryset(self):
        if self.action == "list":
            return Train.objects.all()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return TrainSerializer
        return super().get_serializer_class()
