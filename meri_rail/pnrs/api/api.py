from utils.utils import get_model, format_pnr_details_in_valid_format
from pnrs.api.serializers import PnrNumberSerializer, PnrDetailSerializer
from rest_framework.response import Response
from utils.api_views import BaseAPIView
from utils.constants import SeleniumServices
from http import HTTPStatus
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.utils.timezone import now, timedelta

Pnr = get_model(app_label="pnrs", model_name="Pnr")


@method_decorator(never_cache, name="dispatch")
class PnrApiView(BaseAPIView):
    serializer_class = PnrDetailSerializer
    model = Pnr
    lookup_field = "pnr"

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
        if not pnr_details:
            return self.create(pnr_validation)
        serializer = self.serializer_class(pnr_details)
        if pnr_details.modified < now() - timedelta(minutes=10):
            return self.update(pnr_validation, pnr_details)
        pnr_details.add_user_to_pnr(request.user)
        return Response(serializer.data, status=HTTPStatus.OK)

    def create(self, pnr_validation):
        data = self.use_selenium(data=pnr_validation.validated_data)
        formatted_data = format_pnr_details_in_valid_format(data=data)
        serializer = self.serializer_class(
            data=formatted_data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**formatted_data)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def update(self, pnr_validation, pnr_details):
        data = self.use_selenium(data=pnr_validation.validated_data)
        formatted_data = format_pnr_details_in_valid_format(data=data)
        serializer = self.serializer_class(
            pnr_details, data=formatted_data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(**formatted_data)
        return Response(serializer.data, status=HTTPStatus.OK)
