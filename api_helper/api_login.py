import logging
import os

import allure
import requests
from allure_commons.types import AttachmentType
from dotenv import load_dotenv

from utils.logger import response_attaching, response_logging

logger = logging.getLogger(__name__)

load_dotenv()
URL = os.getenv("URL")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")


class ApiHelper:
    def __init__(self):
        self.session = requests.Session()

    def api_login(self, url=URL, login=LOGIN, password=PASSWORD):
        response = requests.post(
            url=url + "/login",
            data={"Email": login, "Password": password, "RememberMe": False},
            allow_redirects=False,
        )
        response_logging(response)
        response_attaching(response)
        logger.info("Отправили запрос на авторизацию")

        assert (
            "NOPCOMMERCE.AUTH" in response.cookies
        ), "Сервер не вернул куки NOPCOMMERCE.AUTH"
        if "NOPCOMMERCE.AUTH" in response.cookies:
            logger.info("Получена кука NOPCOMMERCE.AUTH")
            allure.attach(
                body=response.cookies.get("NOPCOMMERCE.AUTH"),
                name="NOPCOMMERCE.AUTH Cookie",
                attachment_type=AttachmentType.TEXT,
            )
        return {"NOPCOMMERCE.AUTH": response.cookies.get("NOPCOMMERCE.AUTH")}

    def add_book_in_cart(self, cookies):
        with allure.step("Добавляем книгу в корзину"):
            response = self.session.post(
                url=URL + "/addproducttocart/catalog/22/1/1",
                data={"addtocart_45.EnteredQuantity": "1"},
                headers={"Accept": "application/json"},
                cookies=cookies,
                allow_redirects=False,
            )
            response_logging(response)
            response_attaching(response)
            logger.info("Отправили запрос на добавление книги в корзину")
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление книг в корзину"

        return response.cookies.get("Nop.customer")

    def add_smartphone_and_detail_in_cart(self, cookies):
        with allure.step("Добавляем смартфон и детали в корзину"):
            response = self.session.post(
                url=URL + "/addproducttocart/catalog/43/1/1",
                data={"addtocart_43.EnteredQuantity": "1"},
                headers={"Accept": "application/json"},
                cookies=cookies,
                allow_redirects=False,
            )
            response_logging(response)
            response_attaching(response)
            logger.info("Отправили запрос на добавление смартфона в корзину")
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление смартфона в корзину"

            response = self.session.post(
                url=URL + "/addproducttocart/details/80/1",
                data={
                    "product_attribute_80_2_37": "112",
                    "product_attribute_80_1_38": "114",
                    "addtocart_80.EnteredQuantity": "3",
                },
                headers={"Accept": "application/json"},
                cookies=cookies,
                allow_redirects=False,
            )
            response_logging(response)
            response_attaching(response)
            logger.info("Отправили запрос на добавление детали в корзину")
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление смартфона в корзину"

        return response.cookies.get("Nop.customer")
