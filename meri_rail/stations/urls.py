from rest_framework.routers import SimpleRouter
from stations.api.api import StationViewSet


app_name = "stations"
router = SimpleRouter()
router.register("stations", StationViewSet)
