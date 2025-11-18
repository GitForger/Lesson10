import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple


class CalculatorPage:
    """
    Page Object для страницы "Slow Calculator"
    URL: https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html
    """

    def __init__(self, driver):
        """
        Инициализация Page Object с WebDriver.

        :param driver: Экземпляр WebDriver (Chrome, Firefox и т.д.)
        """
        self.driver = driver
        self._delay_field: Tuple[str, str] = (By.CSS_SELECTOR, "#delay")
        self._result_field: Tuple[str, str] = (By.CSS_SELECTOR, ".screen")
        self._button_locator_template = "//span[contains(@class, 'btn') and text()='{}']"

    @allure.step("Открытие страницы медленного калькулятора")
    def open(self) -> None:
        """Открывает страницу калькулятора."""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    @allure.step("Установка задержки: {delay_seconds} секунд")
    def set_delay(self, delay_seconds: int) -> None:
        """
        Устанавливает значение задержки в поле ввода.

        :param delay_seconds: Количество секунд (целое число)
        :return: None
        """
        delay_input = self.driver.find_element(*self._delay_field)
        delay_input.clear()
        delay_input.send_keys(str(delay_seconds))

    @allure.step("Нажатие кнопки '{button}'")
    def click_button(self, button: str) -> None:
        """
        Нажимает кнопку калькулятора по видимому тексту.

        :param button: Текст на кнопке: '7', '+', '=', 'C' и т.д.
        :return: None
        """
        locator = (By.XPATH, self._button_locator_template.format(button))
        element = self.driver.find_element(*locator)
        element.click()

    @allure.step("Ожидание результата '{expected_result}' на экране")
    def wait_for_result(self, expected_result: str, timeout: int = 50) -> None:
        """
        Ожидает появления точного результата на экране калькулятора.

        :param expected_result: Ожидаемая строка (например, "15")
        :param timeout: Таймаут в секундах (по умолчанию 50)
        :return: None
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(self._result_field, expected_result),
            f"Результат '{expected_result}' не появился за {timeout} секунд"
        )

    @allure.step("Получение текущего значения с экрана")
    def get_result(self) -> str:
        """
        Возвращает текущий текст с экрана калькулятора.

        :return: Строка с результатом
        """
        return self.driver.find_element(*self._result_field).text
