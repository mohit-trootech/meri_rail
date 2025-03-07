from rest_framework.views import APIView
from utils.selenium_service import SeleniumService
from json import loads
from rest_framework.exceptions import ValidationError
from utils.constants import ErrorMessages, SeleniumServices
from utils.utils import log_errors


class BaseAPIView(APIView):
    selenium_service = SeleniumService()
    service = None
    model = None
    driver = None

    def get_service_method(self):
        if SeleniumServices.PNR_STATUS == self.service:
            return self.driver.load_pnr_details
        elif SeleniumServices.FARE_ENQUIRY == self.service:
            return self.driver.fare_enquiry
        elif SeleniumServices.SPOT_TRAIN == self.service:
            return self.driver.spot_train_details
        elif SeleniumServices.SEAT_AVAILABILITY == self.service:
            return self.driver.seat_availability
        raise ValueError(ErrorMessages.INVALID_SERVICE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.model is None:
            raise ValueError(ErrorMessages.MODEL_IS_NONE)
        if self.service is None:
            raise ValueError(ErrorMessages.SERVICE_IS_NONE)

    def use_selenium(self, data: dict):
        self.driver = self.selenium_service
        try:
            captcha = self.driver.validate_captcha()
            service_method = self.get_service_method()
            data = loads(service_method(captcha, data))
        except Exception as err:
            log_errors(__name__, str(err))
            raise ValidationError(
                {"error": ErrorMessages.UNABLE_TO_PROCESS_TRY_AGAIN_LATER}
            )
        finally:
            pass
            # self.driver.driver.quit()
        if "errorMessage" in data:
            if data["errorMessage"] is not None:
                raise ValidationError({"error": data["errorMessage"]})
        return data

    def get_object(self, data):
        try:
            return self.model.objects.get(**data)
        except self.model.DoesNotExist:
            return None
