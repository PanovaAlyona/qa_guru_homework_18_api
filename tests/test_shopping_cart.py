import time

from selene import have, be

from pages.home_page import HomePage



def test_check_books_in_cart(cookies, setup_browser):
    homepage = HomePage()
    homepage.open_cart()
    browser = setup_browser
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookies})
    browser.driver.refresh()




    time.sleep(20)
