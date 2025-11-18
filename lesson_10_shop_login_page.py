import allure
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Page Object для страницы авторизации Swag Labs
    URL: https://www.saucedemo.com/
    """

    def __init__(self, driver: WebDriver):
        """
        Инициализация страницы с WebDriver.

        :param driver: Экземпляр WebDriver
        """
        self.driver = driver
        self._url = "https://www.saucedemo.com/"

        # Локаторы
        self._username_field: Tuple[str, str] = (By.ID, "user-name")
        self._password_field: Tuple[str, str] = (By.ID, "password")
        self._login_button: Tuple[str, str] = (By.ID, "login-button")
        self._error_message: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='error']")
        self._error_button: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='error-button']")

    @allure.step("Открытие страницы авторизации Swag Labs")
    def open(self) -> None:
        """
        Открывает главную страницу авторизации.

        :return: None
        """
        self.driver.get(self._url)
        # Прикрепляем скриншот и URL в Allure
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="login_page_opened",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Ввод логина: {username}")
    def enter_username(self, username: str) -> None:
        """
        Вводит логин в поле username.

        :param username: Логин пользователя (например, 'standard_user')
        :return: None
        """
        field = self.driver.find_element(*self._username_field)
        field.clear()
        field.send_keys(username)

    @allure.step("Ввод пароля: {'*' * len(password)}")  # скрываем пароль в отчёте
    def enter_password(self, password: str) -> None:
        """
        Вводит пароль в поле password.

        :param password: Пароль пользователя
        :return: None
        """
        field = self.driver.find_element(*self._password_field)
        field.clear()
        field.send_keys(password)

    @allure.step("Нажатие кнопки 'Login'")
    def click_login_button(self) -> None:
        """
        Нажимает кнопку Login.

        :return: None
        """
        button = self.driver.find_element(*self._login_button)
        button.click()
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="after_login_click",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Выполнение авторизации: {username} / {password}")
    def login(self, username: str, password: str) -> None:
        """
        Полный логин: заполняет поля и нажимает кнопку.

        :param username: Логин
        :param password: Пароль
        :return: None
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    @allure.step("Получение текста ошибки авторизации")
    def get_error_message(self) -> str:
        """
        Возвращает текст сообщения об ошибке (если есть).

        :return: Текст ошибки (например, "Epic sadface: Username is required")
        """
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._error_message)
        )
        error_text = self.driver.find_element(*self._error_message).text
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="login_error_visible",
            attachment_type=allure.attachment_type.PNG
        )
        return error_text

    @allure.step("Проверка видимости кнопки с крестиком у ошибки")
    def is_error_close_button_visible(self) -> bool:
        """
        Проверяет, видна ли кнопка закрытия ошибки (крестик).

        :return: True — если видна, False — если нет
        """
        return len(self.driver.find_elements(*self._error_button)) > 0