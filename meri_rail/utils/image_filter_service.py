import pytesseract
from PIL import Image
import re
from os.path import join
from django.conf import settings

PAGE_SCREENSHOT = join(settings.BASE_DIR, "fixtures/temp/page_screenshot.png")
CAPTCHA_IMAGE = join(settings.BASE_DIR, "fixtures/temp/captcha.png")


class ImageFiltering:
    """Filter Pnr Image"""

    def __init__(self, image):
        """Captcha Image Filtering Instances"""
        self.image = image

    def get_string_from_image(self):
        """Return Text From Image"""
        return pytesseract.image_to_string(CAPTCHA_IMAGE)

    def crop_captcha_from_ss(self):
        """Crop Captcha from Whole SS"""
        location = self.image.location
        size = self.image.size
        ss = Image.open(PAGE_SCREENSHOT)
        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]
        croped_image = ss.crop((left, top, right, bottom))
        croped_image.save(CAPTCHA_IMAGE)
        return self.get_string_from_image()

    def get_solved_capcha_from_image(self):
        """Return Solved Capcha from Filtered Image"""
        image = self.crop_captcha_from_ss()
        pattern = r"\d+\s*[\+\-\*\/]\s*\d+\s*="
        matches = re.findall(pattern, image)
        return eval(matches[0][:-1])


if __name__ == "__main__":
    pass
