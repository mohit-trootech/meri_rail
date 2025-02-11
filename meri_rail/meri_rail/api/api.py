from rest_framework.views import APIView
from utils.constants import TrainQuota, SeatType, JourneyClass
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from http import HTTPStatus


class BaseChoicesView(APIView):
    permission_classes = [AllowAny]
    choice_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.choice_class is None:
            raise ValueError("choice_class must be set")

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
