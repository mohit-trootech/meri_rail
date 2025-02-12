from spot_train.api.serializers import TrainNumberSerializer
from utils.api_views import BaseAPIView
from utils.constants import SeleniumServices


class SpotTrainView(BaseAPIView):
    service = SeleniumServices.SPOT_TRAIN
    model = "None"

    def get(self, request):
        tn_serializer = TrainNumberSerializer(data=request.data)
        tn_serializer.is_valid(raise_exception=True)
        self.use_selenium(data={})
