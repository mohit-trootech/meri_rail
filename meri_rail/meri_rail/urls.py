from django.contrib import admin
from django.urls import path, include
from trains.urls import router as train_router
from stations.urls import router as station_router
from rest_framework.routers import DefaultRouter
from meri_rail.api.api import (
    train_quota_view,
    journey_class_view,
    seat_type_view,
    mappls_secret_view,
    firestore_configuration_view,
)
from django.conf import settings
from django.conf.urls.static import static
from meri_rail.views import success_view, error_view

router = DefaultRouter()
router.registry.extend(train_router.registry)
router.registry.extend(station_router.registry)


urlpatterns = [
    path("admin-meri-rail/", admin.site.urls),
    path("success/", success_view, name="success"),
    path("error/", error_view, name="error"),
    path("api/", include(router.urls)),
    path("api/train_quota/", train_quota_view, name="train_quota"),
    path("api/journey_class/", journey_class_view, name="journey_class"),
    path("api/seat_type/", seat_type_view, name="seat_type"),
    path("api/", include("pnrs.urls")),
    path("api/", include("fare_enquiry.urls")),
    path("api/", include("trains_between_station.urls")),
    path("api/", include("seat_availability.urls")),
    path("auth/", include("users.urls")),
    path("api/secrets/mappls/", mappls_secret_view, name="mappls"),
    path("api/secrets/firestore/", firestore_configuration_view, name="firestore"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
