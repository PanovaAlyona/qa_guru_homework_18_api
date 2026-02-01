import logging
import os

import allure
from dotenv import load_dotenv
from selene import be, browser, by, have

logger = logging.getLogger(__name__)

load_dotenv()
URL = os.getenv("URL")


class CartPage:
    def open_cart(self, url=URL):
        with allure.step("Открываем страницу с корзиной"):
            logger.info("Открываем страницу корзины")
        browser.open(url + "/cart")

    def set_cookies_and_refresh_browser(
        self, cookies, nop_customer_cookie=None
    ):
        with allure.step("Ставим куки и обновляем браузер"):
            logger.info("Ставим куки и обновляем браузер")
            browser.open(f"{URL}" + "/cart")
            browser.config.driver.add_cookie(
                {
                    "name": "NOPCOMMERCE.AUTH",
                    "value": cookies["NOPCOMMERCE.AUTH"],
                }
            )
            if nop_customer_cookie:
                browser.config.driver.add_cookie(
                    {"name": "Nop.customer", "value": nop_customer_cookie}
                )
            browser.driver.refresh()

    def empty_cart(self, cookies):
        try:
            cart_items = browser.all(".cart-item-row")
            if cart_items.wait_until(have.size_greater_than(0)):
                logger.info(f"Найдено {len(cart_items)} товаров для очистки")

                # Вариант 1:
                qty_inputs = browser.all("input.qty-input")
                for qty_input in qty_inputs:
                    qty_input.clear()
                    qty_input.type("0")

                # Вариант 2:
                update_button = browser.element('input[name="updatecart"]')
                if update_button.wait_until(be.visible):
                    update_button.click()
                    browser.element(".order-summary-content").should(
                        have.text("Your Shopping Cart is empty!")
                    )

                logger.info("Корзина очищена")
            else:
                logger.info("Корзина уже пуста")

        except Exception as e:
            logger.error(f"Ошибка при очистке корзины: {str(e)}")

    def check_product_in_cart(
        self, index, product_name, product_price, product_count
    ):
        with allure.step("Проверяем наличие продукта в корзине"):
            logger.info("Проверяем наличие продуктов в корзине")
            # try:
            #     item = browser.element(
            #             f'//tr[@class="cart-item-row"]//a[contains(@class, "product-name") and contains(text(), '
            #             f'"{product_name}")]'
            #             )
            #     if product_price:
            #         item.element(
            #             '//span[contains(@class, "product-unit-price")]'
            #             )
            #         if product_count:
            #             item.element(
            #                 '//span[contains(@class, "qty-input")]'
            #                 )
            #             logger.info(f"✓ Товар '{product_name}' найден с ценой {product_price}'"
            #                         f"и количеством {product_count}")
            #         else:
            #             logger.error(f"✓ У товара '{product_name}' с ценой {product_price}'"
            #                         f"не корректное количество {product_count}")
            #     return True
            # except Exception:
            #     logger.error(f"✗ Товар '{product_name}' не найден или нет цены/количества")
            #     return False

            with allure.step("Проверяем данные в продуктах"):
                logger.info("Проверяем данные в продуктах")
                browser.element(
                    by.xpath(
                        f"(//*[@class='cart-item-row'])[{index + 1}]//*[@class='product-name']"
                    )
                ).should(have.text(product_name))
                browser.element(
                    by.xpath(
                        f"(//*[@class='cart-item-row'])[{index + 1}]//*[@class='product-unit-price']"
                    )
                ).should(have.text(product_price))
                browser.element(
                    by.xpath(
                        f"(//*[@class='cart-item-row'])[{index + 1}]//*[@class='qty-input']"
                    )
                ).should(have.value(product_count))

    def check_some_products_in_cart(self, products):
        for index, product in enumerate(products):
            self.check_product_in_cart(
                index, product["name"], product["price"], product["count"]
            )
            logger.info(
                f"{product['name']}, {product['price']} - индекс: {index}"
            )
