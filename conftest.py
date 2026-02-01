import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api_helper.api_login import ApiHelper
from pages.cart_page import CartPage

load_dotenv()
URL = os.getenv("URL")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")


@pytest.fixture(scope="session")
def api_login():
    return ApiHelper()


@pytest.fixture(scope="session")
def cookies():
    helper = ApiHelper()
    return helper.api_login()


@pytest.fixture(scope="function")
def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    browser.config.driver = driver

    browser.config.timeout = 10
    browser.config.save_page_source_on_failure = False

    yield browser


@pytest.fixture(scope="function")
def managment_cart(setup_browser, cookies):
    browser = setup_browser
    cart = CartPage()
    yield cart
    cart.empty_cart(cookies)
    browser.quit()
