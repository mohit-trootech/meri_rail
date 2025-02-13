from pathlib import Path
from os.path import join
from utils.constants import Settings, EmailConfig, CeleryConfig
from dj_database_url import config
from django.utils.timezone import timedelta
from dotenv import dotenv_values

env = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Auth User Model
AUTH_USER_MODEL = Settings.AUTH_USER_MODEL
APPEND_SLASH = True

# SECURITY WARNING: keep the secret key used in production secret!
# -------------------------------------------------
SECRET_KEY = env.get("SECRET_KEY")

CITIES_LIGHT_INCLUDE_COUNTRIES = ["IN"]
# Application definition
# -------------------------------------------------
THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
    "corsheaders",
    "email_validator",
    "cities_light",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "django_elasticsearch_dsl",
    "django_filters",
]


# add certificate token
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": [env.get("ELASTIC_HOST", "http://localhost:9200")],
        "http_auth": (
            env.get("ELASTIC_USERNAME", "elastics"),
            env.get("ELASTIC_PASSWORD"),
        ),
    },
}
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = (
    "django_elasticsearch_dsl.signals.RealTimeSignalProcessor"
)
ELASTICSEARCH_DSL_INDEX_SETTINGS = {}
ELASTICSEARCH_DSL_AUTOSYNC = True
ELASTICSEARCH_DSL_AUTO_REFRESH = True
ELASTICSEARCH_DSL_PARALLEL = False
# eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE3LjAuMjo5MjAwIl0sImZnciI6IjFlMzE0M2I5ZWRkMDY3YTEzMmUyODg3Yjc1NWE0MjhkYWEzNTkwZjdjNDI3NWU4OTY1ODBjOGJmMjVmMDhmNTQiLCJrZXkiOiJ0UTBDMnBRQjFRUTY4QS0tZkVRSjpBRzJPVjVFa1RRcUxkaEpkSEJKZ2JnIn0=
PROJECT_APPS = [
    "users.apps.UsersConfig",
    "stations.apps.StationsConfig",
    "trains.apps.TrainsConfig",
    "pnrs.apps.PnrsConfig",
    "fare_enquiry.apps.FareEnquiryConfig",
    "trains_between_station.apps.TrainsBetweenStationConfig",
    "seat_availability.apps.SeatAvailabilityConfig",
    "meri_rail",
]
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS


# Middlewares
# -------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root Urls
# -------------------------------------------------
ROOT_URLCONF = Settings.ROOT_URLCONF

# Templates + Context Processors
# -------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [join(BASE_DIR, Settings.TEMPLATES_URLS)],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI - Web Server Gateway Interface Server
# -------------------------------------------------
WSGI_APPLICATION = Settings.WSGI_APPLICATION


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# -------------------------------------------------
DATABASES = {"default": config(default=env.get("DATABASE_URL"))}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
# -------------------------------------------------
LANGUAGE_CODE = Settings.LANGUAGE_CODE
USE_TZ = True
LANGUAGES = [
    ("en", "English"),
    ("hi", "Hindi"),
]
LOCALE_PATHS = [
    join(BASE_DIR, "locale"),
]

TIME_ZONE = Settings.TIME_ZONE

USE_I18N = Settings.USE_I18N

USE_TZ = Settings.USE_TZ


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# -------------------------------------------------
STATIC_URL = Settings.STATIC_URL
STATICFILES_DIRS = [join(BASE_DIR, Settings.STATIC_FILES_DIRS)]
STATIC_ROOT = join(BASE_DIR, Settings.STATIC_ROOT)

# Media files (Models File)
# -------------------------------------------------
MEDIA_URL = Settings.MEDIA_URL
MEDIA_ROOT = join(BASE_DIR, Settings.MEDIA_ROOT)


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
# -------------------------------------------------
DEFAULT_AUTO_FIELD = Settings.DEFAULT_AUTO_FIELD

# Email Configuration
# =====================================================
EMAIL_BACKEND = EmailConfig.EMAIL_BACKEND
EMAIL_HOST = EmailConfig.EMAIL_HOST
EMAIL_USE_SSL = True  # use port 465
EMAIL_USE_TLS = False  # use port 587
EMAIL_PORT = EmailConfig.PORT_465 if EMAIL_USE_SSL else EmailConfig.PORT_587
EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")

# Rest Framework Configuration
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Celery Configuration
CELERY_BROKER_URL = CeleryConfig.CELERY_BROKER_URL
CELERY_TIMEZONE = Settings.TIME_ZONE
CELERY_RESULT_BACKEND = "redis"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_EXTENDED = True


# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} - {asctime} - {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

# Railway Configuration Urls
# =====================================================
NTES_V1_BASE_URL = env.get("NTES_V1_BASE_URL")
CAPTCHA_DRAW_URL = env.get("CAPTCHA_DRAW_URL")
TRAIN_ROUTE_URL = env.get("TRAIN_ROUTE_URL")
FETCH_TRAIN_DATA_URL = env.get("FETCH_TRAIN_DATA_URL")
PNR_STATUS_URL = env.get("PNR_STATUS_URL")


MODEL_MANAGERS = {"Train": "trains.documents.TrainDocument"}
