from rest_framework.views import APIView
from utils.selenium_service import SeleniumService
from json import loads
from rest_framework.exceptions import ValidationError
from utils.constants import ErrorMessages, SeleniumServices


class BaseAPIView(APIView):
    selenium_service = SeleniumService
    service = None
    model = None
    driver = None

    def get_service_method(self):
        if SeleniumServices.PNR_STATUS == self.service:
            return self.driver.load_pnr_details
        elif SeleniumServices.FARE_ENQUIRY == self.service:
            return self.driver.fare_enquiry
        return None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.model is None:
            raise ValueError("model must not be None")
        if self.service is None:
            raise ValueError("service must not be None")

    def use_selenium(self, data: dict):
        self.driver = self.selenium_service()
        try:
            captcha = self.driver.validate_captcha()
            service_method = self.get_service_method()
            data = loads(service_method(captcha, data))
        except Exception:
            raise ValidationError(
                {"error": ErrorMessages.UNABLE_TO_PROCESS_TRY_AGAIN_LATER}
            )
        finally:
            self.driver.driver.close()
        if "errorMessage" in data:
            raise ValidationError({"error": data["errorMessage"]})
        return data

    def get_object(self, data):
        try:
            return self.model.objects.get(**data)
        except self.model.DoesNotExist:
            return None
