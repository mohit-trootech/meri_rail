from django.conf import settings
from utils.constants import UrlTypesV1, UrlsV1


class UrlServiceV1:
    """Url Service"""

    BASE_URL = settings.NTES_V1_BASE_URL

    @classmethod
    def get_captcha_config_url(cls):
        return cls.BASE_URL + (UrlsV1.CAPTCHA_CONFIG % UrlTypesV1.CAPTCHA_CONFIG)

    @classmethod
    def get_captcha_draw_url(cls, time: str):
        return cls.BASE_URL + (UrlsV1.CAPTCHA_DRAW % (UrlTypesV1.CATPCHA_DRAW, time))

    @classmethod
    def get_train_schedule_url(cls, captcha: str, train: str, time: str):
        return cls.BASE_URL + (UrlsV1.TRAIN_SCHEDULE % (captcha, train, time))

    @classmethod
    def get_pnr_status_url(cls, captcha: str, pnr: str):
        return cls.BASE_URL + (UrlsV1.PNR_STATUS % (captcha, pnr))

    @classmethod
    def get_fare_url(
        cls,
        captcha: str,
        train: str,
        date: str,
        source: str,
        destination: str,
        clas: str,
        quota: str,
        time: str,
    ):
        return cls.BASE_URL + (
            UrlsV1.FARE % (captcha, train, date, source, destination, clas, quota, time)
        )

    @classmethod
    def get_train_between_stations_url(
        cls,
        captcha: str,
        date: str,
        source: str,
        destination: str,
        time: str,
        flexi: str = "n",
    ):
        return cls.BASE_URL + (
            UrlsV1.TRAIN_BETWEEN_STATIONS
            % (captcha, date, source, destination, flexi, time)
        )
