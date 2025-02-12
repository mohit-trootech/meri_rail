from django.utils.translation import gettext_lazy as _


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
    TRAIN_SCHEDULE = "CommonCaptcha?inputCaptcha=%(captcha)s&trainNo=%(train)s&inputPage=TRAIN_SCHEDULE&language=en&_=%(time)s"
    PNR_STATUS = "CommonCaptcha?inputCaptcha=%(captcha)s&inputPnrNo=%(pnr)s&inputPage=PNR&language=en"
    FARE = "CommonCaptcha?inputCaptcha=%(captcha)s&trainNo=%(train)s&dt=%(dt)s&sourceStation=%(from_station)s&destinationStation=%(to_station)s&classc=%(train_cls)s&quota=%(quota)s&inputPage=FARE&language=en&_=%(time)s"
    TRAIN_BETWEEN_STATIONS = "CommonCaptcha?inputCaptcha=%(captcha)s&dt=%(dt)s&sourceStation=%(from_station)s&destinationStation=%(to_station)s&flexiWithDate=n&inputPage=TBIS&language=en&_=%(time)s"


class SeleniumServices:
    """Selenium Services"""

    PNR_STATUS = "pnr_status"
    FARE_ENQUIRY = "fare_enquiry"
    TBIS = "tbis"
    TRAIN_SCHEDULE = "train_schedule"
    SPOT_TRAIN = "spot_train"


class TrainQuota:
    TQ = "TQ"
    LD = "LD"
    DF = "DF"
    FT = "FT"
    SS = "SS"
    PT = "PT"
    YU = "YU"
    DP = "DP"
    HP = "HP"
    PH = "PH"
    GN = "GN"

    CHOICES = (
        (TQ, _("Tatkal Quota")),
        (LD, _("Ladies Quota")),
        (DF, _("Defence Quota")),
        (FT, _("Foreign Tourist Quota")),
        (SS, _("Lower Berth Quota")),
        (PT, _("Premium Tatkal Quota")),
        (YU, _("Yuva Quota")),
        (DP, _("Duty Pass Quota")),
        (HP, _("Handicapped Quota")),
        (PH, _("Parliament House")),
        (GN, _("General Quota")),
    )

    @classmethod
    def get_choice(cls):
        return cls.CHOICES

    @classmethod
    def get_api_choices(cls):
        return {
            cls.TQ: _("Tatkal Quota)"),
            cls.LD: _("Ladies Quota"),
            cls.DF: _("Defence Quota"),
            cls.FT: _("Foreign Tourist Quota"),
            cls.SS: _("Lower Berth Quota"),
            cls.PT: _("Premium Tatkal Quota"),
            cls.YU: _("Yuva Quota"),
            cls.DP: _("Duty Pass Quota"),
            cls.HP: _("Handicapped Quota"),
            cls.PH: _("Parliament House Quota"),
            cls.GN: _("General Quota"),
        }


class JourneyClass:
    FIRST_AC = "1A"
    SECOND_AC = "2A"
    THIRD_AC = "3A"
    THIRD_ECONOMY = "3E"
    SECOND = "2S"
    SL = "SL"
    EC = "EC"
    EA = "EA"
    CC = "CC"
    FC = "FC"
    VS = "VS"
    CH = "CH"
    SH = "SH"
    VC = "VC"
    EV = "EV"

    CHOICES = (
        (FIRST_AC, _("First AC")),
        (SECOND_AC, _("Second AC")),
        (THIRD_AC, _("Third AC")),
        (THIRD_ECONOMY, _("Third AC Economy")),
        (SECOND, _("Second Seating")),
        (SL, _("Sleeper")),
        (EC, _("Executive Class")),
        (EA, _("Executive Anubhuti")),
        (CC, _("AC Chair Car")),
        (FC, _("First Class")),
        (VS, _("Vista Dome Non AC")),
        (CH, _("Chair Car High Capacity")),
        (SH, _("Sleeper High Capacity")),
        (VC, _("Vista Dome CC")),
        (EV, _("Vista Dome AC")),
    )

    @classmethod
    def get_choice(cls):
        return cls.CHOICES

    @classmethod
    def get_api_choices(cls):
        return {
            cls.FIRST_AC: _("First AC"),
            cls.SECOND_AC: _("Second AC"),
            cls.THIRD_AC: _("Third AC"),
            cls.THIRD_ECONOMY: _("Third AC Economy"),
            cls.SECOND: _("Second Seating"),
            cls.SL: _("Sleeper"),
            cls.EC: _("Executive Class"),
            cls.EA: _("Executive Anubhuti"),
            cls.CC: _("AC Chair Car"),
            cls.FC: _("First Class"),
            cls.VS: _("Vista Dome Non AC"),
            cls.CH: _("Chair Car High Capacity"),
            cls.SH: _("Sleeper High Capacity"),
            cls.VC: _("Vista Dome CC"),
            cls.EV: _("Vista Dome AC"),
        }


class SeatType:
    LB = "LB"
    MB = "MB"
    UB = "UB"
    SL = "SL"
    SM = "SM"
    SU = "SU"
    CHOICES = (
        (LB, _("Lower Berth")),
        (MB, _("Middle Berth")),
        (UB, _("Upper Berth")),
        (SL, _("Side Lower")),
        (SM, _("Side Middle")),
        (SU, _("Side Upper")),
    )

    @classmethod
    def get_choice(cls):
        return cls.CHOICES

    @classmethod
    def get_api_choices(cls):
        return {
            cls.LB: _("Lower Berth"),
            cls.MB: _("Middle Berth"),
            cls.UB: _("Upper Berth"),
            cls.SL: _("Side Lower"),
            cls.SM: _("Side Middle"),
            cls.SU: _("Side Upper"),
        }


class TrainType:
    EXP = "EXP"
    RAJ = "RAJ"
    SUP = "SUP"
    RLM = "RLM"
    CHOICES = (
        (EXP, _("Express")),
        (RAJ, _("Rajdhani")),
        (SUP, _("Super")),
        (RLM, _("Regular")),
    )

    @classmethod
    def get_choice(cls):
        return cls.CHOICES


class ErrorMessages:
    NOT_DEFINED = "%s is not defined as class atrribute"
    UNABLE_TO_PROCESS_TRY_AGAIN_LATER = _(
        "Unable to process your request. Please try again later."
    )
    MODEL_IS_NONE = NOT_DEFINED % "Model"
    SERVICE_IS_NONE = NOT_DEFINED % "Service"
    INVALID_SERVICE = _("Invalid Service Defined")


class ValidationErrorConstants:
    DATE_IN_PAST = _("Date must be greater than or equal to today")
    STATION_NOT_FOUND = _("Station not found")
    TRAIN_NOT_FOUND = _("Train not found")
    FROM_TO_STATION_SAME = _("From and to station cannot be same")
    DATE_AFTER_THREE_MONTHS = _("Date cannot be more than 3 months from today")
    INVALID_TRAIN_NUMBER = _("Train number is invalid")
