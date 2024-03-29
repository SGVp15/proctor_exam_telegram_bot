import asyncio
import time
from unittest import TestCase

from ProctorEDU.selenium_for_proctoredu import ProctorEduSelenium


class TestProctorEduSelenium(TestCase):
    def test_authorization(self):
        driver = ProctorEduSelenium()
        asyncio.run(driver.authorization())
        time.sleep(1)
        if driver.driver.current_url != 'https://itexpert.proctoring.online/#!/rooms':
            self.fail()
