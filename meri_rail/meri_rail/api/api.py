from rest_framework.views import APIView
from utils.constants import TrainQuota, SeatType, JourneyClass
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from http import HTTPStatus
from meri_rail.constants import ErrorMessages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings


class MapplsSecretView(APIView):
    def get(self, request):
        token = settings.MAPPLS_API_KEY
        return Response({"token": token}, status=HTTPStatus.OK)


mappls_secret_view = MapplsSecretView.as_view()


@method_decorator(cache_page(60 * 1440), name="dispatch")
class BaseChoicesView(APIView):
    permission_classes = [AllowAny]
    choice_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.choice_class is None:
            raise ValueError(ErrorMessages.CHOICE_CLASS_NOT_SET)

    def get(self, request, *args, **kwargs):
        return Response(self.choice_class.get_api_choices(), status=HTTPStatus.OK)


class TrainQuotaView(BaseChoicesView):
    choice_class = TrainQuota


train_quota_view = TrainQuotaView.as_view()


class JourneyClassView(BaseChoicesView):
    choice_class = JourneyClass


journey_class_view = JourneyClassView.as_view()


class SeatTypeView(BaseChoicesView):
    choice_class = SeatType


seat_type_view = SeatTypeView.as_view()
