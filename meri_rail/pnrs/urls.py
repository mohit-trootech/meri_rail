from django.urls import path
from pnrs.api.api import PnrApiView


app_name = "pnrs"

urlpatterns = [path("pnr/", PnrApiView.as_view(), name="pnr-api")]
