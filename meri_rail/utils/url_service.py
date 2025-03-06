from django.conf import settings
from utils.constants import UrlTypesV1, UrlsV1


class UrlServiceV1:
    """Url Service"""

    BASE_URL = settings.NTES_V1_BASE_URL
    BASE_URL_V2 = settings.NTES_V2_BASE_URL

    @classmethod
    def get_captcha_config_url(cls):
        return cls.BASE_URL + (UrlsV1.CAPTCHA_CONFIG % UrlTypesV1.CAPTCHA_CONFIG)

    @classmethod
    def get_captcha_draw_url(cls, time: str):
        return cls.BASE_URL + (UrlsV1.CAPTCHA_DRAW % (UrlTypesV1.CATPCHA_DRAW, time))

    @classmethod
    def get_train_schedule_url(cls, captcha: str, train: str, time: str):
        return cls.BASE_URL + (
            UrlsV1.TRAIN_SCHEDULE
            % {
                "captcha": captcha,
                "train": train,
                "time": time,
            }
        )

    @classmethod
    def get_pnr_status_url(cls, captcha: str, data: dict):
        data.update({"captcha": captcha})
        return cls.BASE_URL + (UrlsV1.PNR_STATUS % data)

    @classmethod
    def get_fare_url(cls, captcha: str, time: str, data: dict):
        data.update({"captcha": captcha, "time": time})
        return cls.BASE_URL + (UrlsV1.FARE % data)

    @classmethod
    def get_tbis_url(cls, captcha: str, time: str, data: dict):
        data.update(
            {
                "captcha": captcha,
                "time": time,
            }
        )
        return cls.BASE_URL + (UrlsV1.TRAIN_BETWEEN_STATIONS % data)

    @classmethod
    def get_spot_train_url(cls):
        return cls.BASE_URL + (UrlsV1.SPOT_TRAIN % UrlTypesV1.SPOT_TRAIN)

    @classmethod
    def get_seat_availability(cls, captcha: str, time: str, data: dict):
        data.update(
            {
                "captcha": captcha,
                "time": time,
            }
        )
        return cls.BASE_URL + (UrlsV1.SEAT_AVAILABILITY % data)

    @classmethod
    def get_live_status_url(cls):
        return cls.BASE_URL_V2
