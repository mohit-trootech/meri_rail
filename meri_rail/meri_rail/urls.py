from django.contrib import admin
from django.urls import path, include
from trains.urls import router as train_router
from stations.urls import router as station_router
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls
from meri_rail.api.api import train_quota_view, journey_class_view, seat_type_view

router = DefaultRouter()
router.registry.extend(train_router.registry)
router.registry.extend(station_router.registry)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/train_quota/", train_quota_view, name="train_quota"),
    path("api/journey_class/", journey_class_view, name="journey_class"),
    path("api/seat_type/", seat_type_view, name="seat_type"),
    path("api/", include("pnrs.urls")),
    path("api/", include("fare_enquiry.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
