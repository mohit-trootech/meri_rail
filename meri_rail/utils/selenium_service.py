from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.conf import settings
from utils.image_filter_service import ImageFiltering
from os.path import join


PAGE_SCREENSHOT = join(settings.BASE_DIR, "fixtures/temp/page_screenshot.png")


class SeleniumService:
    CAPTCHA_DRAW_URL = settings.CAPTCHA_DRAW_URL
    TRAIN_ROUTE_URL = settings.TRAIN_ROUTE_URL
    FETCH_TRAIN_DATA_URL = settings.FETCH_TRAIN_DATA_URL
    PNR_STATUS_URL = settings.PNR_STATUS_URL

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
        self.driver.get(self.CAPTCHA_DRAW_URL % self.time)
        image = self.driver.find_element(By.TAG_NAME, "img")
        self.driver.save_screenshot(PAGE_SCREENSHOT)
        image_filter = ImageFiltering(image)
        solved_captcha = image_filter.get_solved_capcha_from_image()
        return solved_captcha

    def load_train_details(self, captcha: int, train: str):
        """load train details"""
        self.driver.get(self.TRAIN_ROUTE_URL % (captcha, train, self.time))
        return self.get_json()

    def load_pnr_details(self, captcha: int, pnr: int):
        """load pnr details"""
        self.driver.get(self.PNR_STATUS_URL % (captcha, pnr))
        return self.get_json()
