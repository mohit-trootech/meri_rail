# Settings Constants
# =====================================================
class Settings:
    """Settings Constants"""

    ROOT_URLCONF = "meri_rail.urls"
    AUTH_USER_MODEL = "users.User"
    WSGI_APPLICATION = "meri_rail.wsgi.application"
    ASGI_APPLICATION = "meri_rail.asgi.application"
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


# NTES Configuration Constants
class UrlTypesV1:
    """NTES V1 Url Types"""

    FETCH_TRAIN_DATA = "FetchTrainData"
    CATPCHA_DRAW = "captchaDraw.png"
    CAPTCHA_CONFIG = "CaptchaConfig"


class UrlsV1:
    """NTES V1 Urls"""

    CAPTCHA_CONFIG = "%s"
    CAPTCHA_DRAW = "%s?%s"
    TRAIN_SCHEDULE = "CommonCaptcha?inputCaptcha=%s&trainNo=%s&inputPage=TRAIN_SCHEDULE&language=en&_=%s"
    PNR_STATUS = "CommonCaptcha?inputCaptcha=%s&inputPnrNo=%s&inputPage=PNR&language=en"
    FARE = "CommonCaptcha?inputCaptcha=%s&trainNo=%s&dt=%s&sourceStation=%s&destinationStation=%s&classc=%s&quota=%s&inputPage=FARE&language=en&_=%s"
    TRAIN_BETWEEN_STATIONS = "CommonCaptcha?inputCaptcha=%s&dt=%s&sourceStation=%s&destinationStation=%s&flexiWithDate=%s&inputPage=TBIS&language=en&_=%s"
