from django.urls import path
from seat_availability.api.api import seat_availability_view

urlpatterns = [
    path("seat-availability/", seat_availability_view, name="seat_availability"),
]
