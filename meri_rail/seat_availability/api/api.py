from utils.api_views import BaseAPIView
from utils.constants import SeleniumServices
from seat_availability.api.serializer import (
    SeatAvailabilitySerializer,
    SeatAvailabilityFilterSerializer,
)
from utils.utils import get_model
from utils.format_data import format_seat_availability
from http import HTTPStatus
from rest_framework.response import Response
from django.utils.timezone import timedelta, now
from django.core.cache import cache
from seat_availability.constants import SEAT_AVAILABILITY_CACHE


SeatAvailability = get_model(
    app_label="seat_availability", model_name="SeatAvailability"
)


class SeatAvailabilityAPIView(BaseAPIView):
    queryset = SeatAvailability.objects.filter(dt__gte=now().date())
    service = SeleniumServices.SEAT_AVAILABILITY
    model = SeatAvailability
    serializer_class = SeatAvailabilitySerializer
    filter_serializer_class = SeatAvailabilityFilterSerializer

    def seat_availability_scrap(self, filter_serializer):
        data = self.use_selenium(filter_serializer.validated_data)
        formatted_data = format_seat_availability(
            data=data, **filter_serializer.validated_data
        )
        return formatted_data

    def create(self, filter_serializer):
        formatted_data = self.seat_availability_scrap(filter_serializer)
        serializer = self.serializer_class(
            data=formatted_data, many=True, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.set(
            SEAT_AVAILABILITY_CACHE % filter_serializer.validated_data,
            serializer.data,
            timeout=60 * 10,
        )
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def update(self, filter_serializer, qs):
        formatted_data = self.seat_availability_scrap(filter_serializer)
        serializer = self.serializer_class(
            qs, data=formatted_data, many=True, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.set(
            SEAT_AVAILABILITY_CACHE % filter_serializer.validated_data,
            serializer.data,
            timeout=60 * 10,
        )
        return Response(serializer.data, status=HTTPStatus.OK)

    def get(self, request, *args, **kwargs):
        filter_serializer = self.filter_serializer_class(data=request.data)
        filter_serializer.is_valid(raise_exception=True)
        dates = [
            (
                now().strptime(self.request.data["dt"], "%Y-%m-%d")
                + timedelta(days=counter)
            ).strftime("%Y-%m-%d")
            for counter in range(6)
        ]
        cache_data = cache.get(
            SEAT_AVAILABILITY_CACHE % filter_serializer.validated_data,
        )
        if cache_data:
            return Response(cache_data, status=HTTPStatus.OK)
        qs = self.queryset.filter(
            **{
                "train__number": request.data["train"],
                "quota": request.data["quota"],
                "train_cls": request.data["train_cls"],
                "dt__in": dates,
            }
        )
        if not qs:
            return self.create(filter_serializer=filter_serializer)
        if not qs.filter(modified__gte=now() - timedelta(minutes=10)):
            return self.update(filter_serializer=filter_serializer, qs=qs)
        serializer = self.serializer_class(qs, many=True)
        cache.set(
            SEAT_AVAILABILITY_CACHE % filter_serializer.validated_data,
            serializer.data,
            60 * 10,
        )
        return Response(serializer.data, status=HTTPStatus.OK)


seat_availability_view = SeatAvailabilityAPIView.as_view()
