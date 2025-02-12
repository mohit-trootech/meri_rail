from utils.api_views import BaseAPIView
from utils.utils import get_model
from trains_between_station.api.serializer import (
    TrainBetweenStationSerializer,
    TbisSerializer,
)
from utils.format_data import format_tbis_trains_list
from utils.constants import SeleniumServices
from http import HTTPStatus
from rest_framework.response import Response


TrainsList = get_model(app_label="trains_between_station", model_name="TrainsList")
TrainBetweenStation = get_model(
    app_label="trains_between_station", model_name="TrainBetweenStation"
)


class TrainBetweenStationApiView(BaseAPIView):
    model = TrainBetweenStationSerializer
    service = SeleniumServices.TBIS
    permission_classes = []  # TODO : Remove allow any

    def get(self, request):
        tbis_serializer = TbisSerializer(data=request.data)
        tbis_serializer.is_valid(raise_exception=True)
        return self.create(tbis_serializer)

    def create(self, tbis_serializer):
        data = self.use_selenium(data=tbis_serializer.validated_data)
        tbis_formatted = format_tbis_trains_list(data)
        tbis_serializer = TrainBetweenStationSerializer(data=tbis_formatted, many=True)
        tbis_serializer.is_valid(raise_exception=True)
        tbis_serializer.save()
        return Response(tbis_serializer.data, status=HTTPStatus.CREATED)


train_between_station_view = TrainBetweenStationApiView.as_view()
