from django.urls import path
from fare_enquiry.api.api import fare_view


app_name = "fare"
urlpatterns = [
    path("fare/", fare_view, name="fare"),
]
