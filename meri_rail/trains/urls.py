from trains.api.api import (
    TrainViewSet,
)
from rest_framework.routers import SimpleRouter

app_name = "trains"
router = SimpleRouter()
router.register("trains", TrainViewSet)
