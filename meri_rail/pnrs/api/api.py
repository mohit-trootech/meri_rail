from rest_framework.views import APIView
from utils.utils import get_model, format_pnr_details_in_valid_format
from pnrs.api.serializers import PnrNumberSerializer, PnrDetailSerializer
from utils.selenium_service import SeleniumService
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from json import loads


Pnr = get_model(app_label="pnrs", model_name="Pnr")


class PnrApiView(APIView):
    queryset = Pnr.objects.all()
    serializer_class = PnrDetailSerializer
    selenium_service = SeleniumService
    lookup_field = "pnr"

    def use_selenium(self, pnr):
        driver = self.selenium_service()
        try:
            captcha = driver.validate_captcha()
            return loads(driver.load_pnr_details(captcha, pnr))
        except Exception:
            return
        finally:
            driver.driver.close()

    def post(self, request, *args, **kwargs):
        pnr_ser = PnrNumberSerializer(data=request.data)
        pnr_ser.is_valid(raise_exception=True)
        pnr = pnr_ser.validated_data["pnr"]
        try:
            pnr_obj = Pnr.objects.get(pnr=pnr)
            serializer = self.serializer_class(pnr_obj)
            return Response(serializer.data)
        except Pnr.DoesNotExist:
            data = self.use_selenium(pnr=pnr)
            if data is None:
                raise ValidationError(
                    {
                        "message": "Unable to process the request at this moment. Please try again later."
                    }
                )
            if "errorMessage" in data:
                raise ValidationError({"message": data["errorMessage"]})
            validated_data = format_pnr_details_in_valid_format(data=data)
            serializer = self.serializer_class(data=validated_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(**validated_data)
            return Response(serializer.data)
