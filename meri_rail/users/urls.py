"""Users Urls"""

from users.api.api import UserProfileView, GoogleAuthServiceView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("google", GoogleAuthServiceView, basename="google-auth")
router.register("profile", UserProfileView, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]
