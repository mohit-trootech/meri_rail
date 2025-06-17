from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from users.constants import (
    THUMBNAIL_PREVIEW_TAG,
    THUMBNAIL_PREVIEW_HTML,
)
from django.utils.html import format_html
from django_extensions.db.models import TimeStampedModel
from users.constants import VerboseNames, ModelFields


def _upload_to(self, filename):
    """Upload User Profile Image"""
    return "users/{username}/{filename}".format(
        username=self.username, filename=filename
    )


def _random_otp(self):
    import random

    return random.randint(100000, 999999)


class User(AbstractUser):
    """Abstract User Model"""

    image = models.ImageField(
        verbose_name=VerboseNames.PROFILE_IMAGE,
        upload_to=_upload_to,
        blank=True,
        null=True,
    )
    email = models.EmailField(verbose_name=VerboseNames.EMAIL_ADDRESS, unique=True)
    age = models.IntegerField(verbose_name=VerboseNames.AGE, blank=True, null=True)
    address = models.TextField(verbose_name=VerboseNames.ADDRESS, blank=True, null=True)
    google_id = models.CharField(
        blank=True,
        null=True,
        verbose_name=VerboseNames.GOOGLE_ID,
        unique=True,
        max_length=255,
    )
    activity_status = models.BooleanField(
        verbose_name=VerboseNames.ACTIVITY_STATUS,
        choices=ModelFields.STATUS_CHOICES,
        default=ModelFields.ACTIVE_STATUS,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def profile_image(self):
        """Profile Image Viewer"""
        if self.image:
            return format_html(THUMBNAIL_PREVIEW_TAG.format(img=self.image.url))
        return format_html(THUMBNAIL_PREVIEW_HTML)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy("user:details", kwargs={"username": self.username})

    @property
    def get_credentials(self):
        google_oauth_token = self.googleoauth2token
        return {
            "access_token": google_oauth_token.access_token,
            "refresh_token": google_oauth_token.refresh_token,
            "expires_at": google_oauth_token.expires_at.isoformat() + "Z",
        }


class Otp(TimeStampedModel):
    """OTP Models to Store OTP Details"""

    otp = models.IntegerField(default=_random_otp)
    expiry = models.DateTimeField()
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="otp"
    )

    def __str__(self):
        return "{user}'s OTP".format(user=self.user.username)


class GoogleOAuth2Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField()
