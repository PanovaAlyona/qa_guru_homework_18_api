import os
import logging

import allure
from dotenv import load_dotenv
from selene import browser

logger = logging.getLogger(__name__)

load_dotenv()
URL = os.getenv("URL")
class HomePage:
    def open_cart(self,url=URL):
        with allure.step("Открываем страницу с корзиной"):
            logger.info("Открываем страницу корзины")
        browser.open(url + "/cart")

