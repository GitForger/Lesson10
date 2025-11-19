import allure
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.CartPage import CartPage


class ProductsPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._cart_link = (By.CLASS_NAME, "shopping_cart_link")
        self._add_to_cart_template = (
            "//div[normalize-space(.)='{}']/ancestor::div[@class='inventory_item_description']//button"
        )

    @allure.step("Добавление товара в корзину: {product_name}")
    def add_product_to_cart(self, product_name: str) -> None:
        locator = (By.XPATH, self._add_to_cart_template.format(product_name))
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        btn.click()

    @allure.step("Переход в корзину")
    def go_to_cart(self) -> CartPage:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._cart_link)
        ).click()

        return CartPage(self.driver)


