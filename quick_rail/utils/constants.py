# Settings Constants
# =====================================================
class Settings:
    """Settings Constants"""

    ROOT_URLCONF = "quick_rail.urls"
    AUTH_USER_MODEL = "users.User"
    WSGI_APPLICATION = "quick_rail.wsgi.application"
    ASGI_APPLICATION = "quick_rail.asgi.application"
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Asia/Kolkata"
    USE_I18N = True
    USE_TZ = True
    STATIC_URL = "static/"
    STATIC_ROOT = "assets/"
    STATIC_FILES_DIRS = "static/"
    TEMPLATES_URLS = "templates/"
    MEDIA_URL = "media/"
    MEDIA_ROOT = "media/"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email Configurations
# =====================================================
class EmailConfig:
    """Email Configurations"""

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    PORT_465 = 465
    PORT_587 = 587


# Celery Configuration
# =====================================================
class CeleryConfig:
    """Celery Configuration"""

    CELERY_BROKER_URL = "redis://localhost:6379/0"
