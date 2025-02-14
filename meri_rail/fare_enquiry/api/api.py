from fare_enquiry.api.serializers import (
    FareEnquirySerializer,
    FareSerializer,
)
from utils.utils import get_model, format_fare_serializer
from rest_framework.response import Response
from utils.api_views import BaseAPIView
from http import HTTPStatus
from utils.constants import SeleniumServices
from django.core.cache import cache
from fare_enquiry.constants import CACHE_KEY

Fare = get_model(app_label="fare_enquiry", model_name="Fare")


class FareView(BaseAPIView):
    model = Fare
    serializer_class = FareEnquirySerializer
    service = SeleniumServices.FARE_ENQUIRY

    def get(self, request):
        """
        get method to fetch fare details from database if exist else fetch from selenium
        """
        enquiry_serializer = FareEnquirySerializer(data=request.data)
        enquiry_serializer.is_valid(raise_exception=True)
        cache_data = cache.get(CACHE_KEY % enquiry_serializer.validated_data)
        if cache_data:
            fare_serializer = FareSerializer(cache_data)
            return Response(fare_serializer.data)
        fare = self.get_object(
            {
                "train__number": request.data["train"],
                "from_station__code": request.data["from_station"],
                "to_station__code": request.data["to_station"],
                "quota": request.data["quota"],
                "train_cls": request.data["train_cls"],
            }
        )
        if fare:
            fare_serializer = FareSerializer(fare)
            return Response(fare_serializer.data)
        return self.create(enquiry_serializer)

    def create(self, enquiry_serializer):
        data = self.use_selenium(data=enquiry_serializer.validated_data)
        formatted_data = format_fare_serializer(data=data, payload=self.request.data)
        fare_serializer = FareSerializer(data=formatted_data)
        fare_serializer.is_valid(raise_exception=True)
        fare_serializer.save(**formatted_data)
        cache.set(CACHE_KEY % enquiry_serializer.validated_data, fare_serializer.data)
        return Response(fare_serializer.data, status=HTTPStatus.CREATED)


fare_view = FareView.as_view()
