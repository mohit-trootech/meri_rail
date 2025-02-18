from django.contrib import admin
from django.urls import path, include
from trains.urls import router as train_router
from stations.urls import router as station_router
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls
from meri_rail.api.api import train_quota_view, journey_class_view, seat_type_view
from django.conf import settings
from django.conf.urls.static import static

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
    path("api/", include("trains_between_station.urls")),
    path("api/", include("seat_availability.urls")),
    path("auth/", include("users.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
