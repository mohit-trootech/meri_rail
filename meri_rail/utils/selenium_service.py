from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.conf import settings
from utils.image_filter_service import ImageFiltering
from os.path import join
from utils.url_service import UrlServiceV1

PAGE_SCREENSHOT = join(settings.BASE_DIR, "fixtures/temp/page_screenshot.png")


class SeleniumService:
    """Selenium Service Class"""

    url_service = UrlServiceV1

    def __init__(self):
        self.time = round(time() * 1000)
        options = webdriver.FirefoxOptions()
        options.set_preference("devtools.jsonview.enabled", False)
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def get_json(self):
        counter = 0
        while True:
            try:
                if counter > 5:
                    return
                return self.driver.find_element(By.TAG_NAME, "pre").text
            except Exception:
                counter += 1

    def validate_captcha(self):
        """load captcha page"""
        self.driver.get(self.url_service.get_captcha_draw_url(time=self.time))
        image = self.driver.find_element(By.TAG_NAME, "img")
        self.driver.save_screenshot(PAGE_SCREENSHOT)
        image_filter = ImageFiltering(image)
        solved_captcha = image_filter.get_solved_capcha_from_image()
        return solved_captcha

    def load_train_details(self, captcha: str, train: str):
        """load train details"""
        self.driver.get(
            self.url_service.get_train_schedule_url(
                captcha=captcha, train=train, time=self.time
            )
        )
        return self.get_json()

    def load_pnr_details(self, captcha: str, data: dict):
        """load pnr details"""
        self.driver.get(self.url_service.get_pnr_status_url(captcha=captcha, data=data))
        return self.get_json()

    def fare_enquiry(self, captcha: str, data: dict):
        """
        fare enquiry
        """
        self.driver.get(
            self.url_service.get_fare_url(
                captcha=captcha,
                time=self.time,
                data=data,
            )
        )
        return self.get_json()

    def seat_availability(self, captcha: str, data: dict):
        """
        tbis details
        """
        self.driver.get(
            self.url_service.get_seat_availability(
                captcha=captcha,
                time=self.time,
                data=data,
            )
        )
        return self.get_json()

    def spot_train_details(self, captcha: str, data: dict):
        """
        spot train details
        """
        self.driver.get(
            self.url_service.get_spot_train_url(
                captcha=captcha,
                time=self.time,
                data=data,
            )
        )
