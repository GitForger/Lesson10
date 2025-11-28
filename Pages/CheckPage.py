import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """
    Page Object для страницы оформления заказа (Your Information + Overview)
    """

    def __init__(self, driver: WebDriver):
        """
        :param driver: WebDriver
        """
        self.driver = driver
        self._first_name = (By.ID, "first-name")
        self._last_name = (By.ID, "last-name")
        self._postal_code = (By.ID, "postal-code")
        self._continue_btn = (By.ID, "continue")
        self._total_label = (By.CLASS_NAME, "summary_total_label")

    @allure.step("Заполнение формы оформления: {first_name} {last_name}, {postal_code}")
    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Заполняет форму и нажимает Continue.

        :param first_name: Имя
        :param last_name: Фамилия
        :param postal_code: Почтовый индекс
        :return: None
        """
        self.driver.find_element(*self._first_name).send_keys(first_name)
        self.driver.find_element(*self._last_name).send_keys(last_name)
        self.driver.find_element(*self._postal_code).send_keys(postal_code)
        self.driver.find_element(*self._continue_btn).click()

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="checkout_overview",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Получение итоговой суммы")
    def get_total_amount(self) -> str:
        """
        Возвращает итоговую сумму без префикса 'Total: $'.

        :return: Строка с суммой, например "58.29"
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._total_label)
        )
        total_text = self.driver.find_element(*self._total_label).text
        return total_text.replace("Total: $", "")