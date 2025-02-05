from django.contrib import admin
from django.urls import path, include
from trains.urls import router as train_router
from stations.urls import router as station_router
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()
router.registry.extend(train_router.registry)
router.registry.extend(station_router.registry)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include("pnrs.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()
