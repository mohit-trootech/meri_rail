from utils.api_views import BaseAPIView
from utils.utils import get_model
from trains_between_station.api.serializer import (
    TbisSerializer,
    TrainBetweenStationSerializer,
)
from utils.constants import SeleniumServices
from http import HTTPStatus
from rest_framework.response import Response
from utils.tbis_queryset import find_trains_between_stations

Route = get_model(app_label="trains", model_name="Route")


class TrainBetweenStationApiView(BaseAPIView):
    service = SeleniumServices.TBIS
    permission_classes = []  # TODO : Remove allow any
    model = "He"

    def get(self, request):
        tbis_serializer = TbisSerializer(data=request.data)
        tbis_serializer.is_valid(raise_exception=True)
        qs = find_trains_between_stations(
            station_from_code=tbis_serializer.validated_data["from_station"],
            station_to_code=tbis_serializer.validated_data["to_station"],
            date=tbis_serializer.validated_data["dt"],
        )
        serializer = TrainBetweenStationSerializer(
            {"trains": qs, **tbis_serializer.validated_data}
        )
        return Response(serializer.data, status=HTTPStatus.OK)


train_between_station_view = TrainBetweenStationApiView.as_view()
