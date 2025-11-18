import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lesson_10_shop_check import CheckoutPage


class CartPage:
    """
    Page Object для страницы корзины
    """

    def __init__(self, driver: WebDriver):
        """
        Инициализация страницы корзины.

        :param driver: Экземпляр WebDriver
        """
        self.driver = driver
        self._checkout_btn = (By.ID, "checkout")

    @allure.step("Нажатие кнопки Checkout")
    def click_checkout(self) -> CheckoutPage:
        """
        Нажимает кнопку Checkout и переходит на страницу оформления.

        :return: Экземпляр CheckoutPage
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._checkout_btn)
        ).click()
        return CheckoutPage(self.driver)
