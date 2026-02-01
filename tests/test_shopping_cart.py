import allure


@allure.epic("Добавление товаров в корзину")
@allure.title("Добавить один товар")
def test_check_book_in_cart(cookies, managment_cart, api_login):
    products = {"name": "Health Book", "price": "10.00", "count": "1"}

    get_cookies_after_add_product = api_login.add_book_in_cart(cookies)

    managment_cart.set_cookies_and_refresh_browser(
        cookies, get_cookies_after_add_product
    )
    managment_cart.check_product_in_cart(
        0, products["name"], products["price"], products["count"]
    )


@allure.epic("Добавление товаров в корзину")
@allure.title("Добавить добавить два товара")
def test_check_electronik_in_cart(cookies, managment_cart, api_login):
    products = [
        {"name": "Smartphone", "price": "100.00", "count": "1"},
        {"name": "Phone Cover", "price": "10.00", "count": "3"},
    ]

    get_cookies_after_add_product = (
        api_login.add_smartphone_and_detail_in_cart(cookies)
    )
    managment_cart.set_cookies_and_refresh_browser(
        cookies, get_cookies_after_add_product
    )
    managment_cart.check_some_products_in_cart(products)
