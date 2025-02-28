from settings.base import *  # noqa
from settings.base import INSTALLED_APPS, MIDDLEWARE, env

INSTALLED_APPS += ["storages", "whitenoise.runserver_nostatic"]
MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
DEBUG = False
ALLOWED_HOSTS = [
    "3.110.47.167",
    "http://127.0.0.1/",
    "ec2-3-110-47-167.ap-south-1.compute.amazonaws.com",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.0.31:3000",
    "https://meri-rail-web.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True

# DEFAULT_FILE_STORAGE = "settings.storage_backends.MediaStorage"
# STATICFILES_STORAGE = "settings.storage_backends.StaticStorage"
# AWS S3 Configurations
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "settings.storage.StaticStorage",
        "OPTIONS": {
            "location": "static",
            "file_overwrite": False,
        },
    },
    "media": {
        "BACKEND": "settings.storage.MediaStorage",
        "OPTIONS": {
            "location": "media",
            "file_overwrite": False,
        },
    },
}
AWS_ACCESS_KEY_ID = env.get("AWS_S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.get("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "merirail"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_SIGNATURE_NAME = "s3v4"
AWS_S3_REGION_NAME = "ap-south-1"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_S3_ADDRESSING_STYLE = "auto"

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
AWS_S3_SECURE_URLS = True
