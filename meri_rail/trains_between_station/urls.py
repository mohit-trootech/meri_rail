from django.urls import path
from trains_between_station.api.api import train_between_station_view

app_name = "tbis"
urlpatterns = [path("tbis/", train_between_station_view)]
