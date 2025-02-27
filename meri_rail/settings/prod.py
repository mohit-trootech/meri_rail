from settings.base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*", "http://127.0.0.1/"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://192.168.0.31:3000",
    "https://meri-rail-web.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True
