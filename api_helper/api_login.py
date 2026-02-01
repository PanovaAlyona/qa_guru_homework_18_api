import os
import logging

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
URL = os.getenv("URL")
LOGIN = os.getenv("LOGIN")
PASSWORD =os.getenv("PASSWORD")
class ApiHelper:
    def __init__(self):
        self.session = requests.Session()

    def api_login(self, url=URL, login=LOGIN, password=PASSWORD):
        response = requests.post(
                    url=url + "/login",
                    data={"Email": login, "Password": password, "RememberMe": False},
                    allow_redirects=False
                )
    #чужой код
        logger.info("Отправили запрос на авторизацию")

        #self.log_request_and_response(response.request, response)
        assert (
                "NOPCOMMERCE.AUTH" in response.cookies
        ), "Сервер не вернул куки NOPCOMMERCE.AUTH"
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        return cookie

    #def cookies(self):

