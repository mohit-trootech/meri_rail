from rest_framework.views import APIView
from utils.socket_service import SocketService
from rest_framework.exceptions import ValidationError
from utils.constants import ErrorMessages, SocketServices
from utils.utils import log_errors


class BaseAPIView(APIView):
    service_class = SocketService
    service = None
    model = None
    driver = None

    def get_service_method(self):
        if SocketServices.PNR_STATUS == self.service:
            return self.service_class.pnr_service
        elif SocketServices.FARE_ENQUIRY == self.service:
            return self.service_class.fare_service
        elif SocketServices.SPOT_TRAIN == self.service:
            return self.service_class.spot_train_service
        elif SocketServices.SEAT_AVAILABILITY == self.service:
            return self.service_class.seat_availability_service
        raise ValueError(ErrorMessages.INVALID_SERVICE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.model is None:
            raise ValueError(ErrorMessages.MODEL_IS_NONE)
        if self.service is None:
            raise ValueError(ErrorMessages.SERVICE_IS_NONE)

    def use_socket_service(self, data: dict):
        try:
            service_method = self.get_service_method()
            data = service_method(data=data)
            return data
        except Exception as err:
            log_errors(__name__, str(err))
            raise ValidationError(
                {"error": ErrorMessages.UNABLE_TO_PROCESS_TRY_AGAIN_LATER}
            )
        finally:
            pass

    def get_object(self, data):
        try:
            return self.model.objects.get(**data)
        except self.model.DoesNotExist:
            return None
