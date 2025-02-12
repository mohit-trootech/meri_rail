from utils.utils import get_model, format_pnr_details_in_valid_format
from pnrs.api.serializers import PnrNumberSerializer, PnrDetailSerializer
from rest_framework.response import Response
from utils.api_views import BaseAPIView
import rest_framework
from utils.constants import SeleniumServices
from http import HTTPStatus

Pnr = get_model(app_label="pnrs", model_name="Pnr")


class PnrApiView(BaseAPIView):
    serializer_class = PnrDetailSerializer
    model = Pnr
    lookup_field = "pnr"
    permission_classes = [
        rest_framework.permissions.AllowAny
    ]  # TODO: remove permissions
    service = SeleniumServices.PNR_STATUS

    def get(self, request, *args, **kwargs):
        """
        get method that uses request payload to fetch the pnr details from database if exist else use selenium.
        """
        pnr_validation = PnrNumberSerializer(data=request.data)
        pnr_validation.is_valid(raise_exception=True)
        pnr_details = self.get_object(
            data={"pnr": pnr_validation.validated_data["pnr"]}
        )
        if pnr_details:
            serializer = self.serializer_class(pnr_details)
            return Response(serializer.data, status=HTTPStatus.OK)
        return self.create(pnr_validation)

    def create(self, pnr_validation):
        data = self.use_selenium(data=pnr_validation.validated_data)
        formatted_data = format_pnr_details_in_valid_format(data=data)
        serializer = self.serializer_class(data=formatted_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**formatted_data)
        return Response(serializer.data, status=HTTPStatus.CREATED)
