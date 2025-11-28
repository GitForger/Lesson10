import allure
import pytest
from Pages.LoginPage import LoginPage
from Pages.ProductPage import ProductsPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Swag Labs")
@allure.title("Полный сценарий покупки: 3 товара → Checkout → Проверка суммы")
@allure.description(
    "Авторизация → Добавление 3 товаров → Корзина → Оформление → Проверка Total = 58.29"
)
@allure.severity(allure.severity_level.CRITICAL)
def test_full_checkout_flow(driver):
    login_page = LoginPage(driver)
    products_page = ProductsPage(driver)

    with allure.step("1. Открываем сайт и логинимся как standard_user"):
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

    with allure.step("2. Добавляем 3 товара в корзину"):
        products_page.add_product_to_cart("Sauce Labs Backpack")
        products_page.add_product_to_cart("Sauce Labs Bolt T-Shirt")
        products_page.add_product_to_cart("Sauce Labs Onesie")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="three_items_in_cart",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step("3. Переходим в корзину"):
        cart_page = products_page.go_to_cart()

    with allure.step("4. Нажимаем Checkout"):
        checkout_page = cart_page.click_checkout()

    with allure.step("5. Заполняем форму оформления"):
        checkout_page.fill_checkout_form("Иван", "Иванов", "123456")

    with allure.step("6. Проверяем итоговую сумму"):
        total = checkout_page.get_total_amount()
        assert total == "58.29", f"Ожидалась сумма 58.29, а получено: {total}"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="shop_result",
            attachment_type=allure.attachment_type.PNG
        )
