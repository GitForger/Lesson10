import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lesson_10_calc_base import CalculatorPage


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Медленный калькулятор")
@allure.title("Проверка сложения 7 + 8 с задержкой 45 секунд")
@allure.description(
    """
    Тест проверяет корректность работы медленного калькулятора.
    Устанавливаем delay = 45 сек → вводим 7 + 8 = → ждём результат 15
    """
)
@allure.severity(allure.severity_level.CRITICAL)
def test_calculator_with_delay(driver):
    calc = CalculatorPage(driver)

    with allure.step("Открываем страницу калькулятора"):
        calc.open()

    with allure.step("Устанавливаем задержку 45 секунд"):
        calc.set_delay(45)

    with allure.step("Вводим выражение: 7 + 8 ="):
        calc.click_button("7")
        calc.click_button("+")
        calc.click_button("8")
        calc.click_button("=")

    with allure.step("Ожидаем результат '15'"):
        calc.wait_for_result("15")

    with allure.step("Проверяем, что результат действительно 15"):
        assert calc.get_result() == "15", f"Ожидали 15, а получили {calc.get_result()!r}"