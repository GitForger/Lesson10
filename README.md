Тесты выполнялись на Chrome Версия 129.0.6668.60 (Официальная сборка), (64 бит)

## Как запустить
```bash
# из папки D:\10_Lesson
pip install -r requirements.txt

# все тесты сразу
pytest

# только калькулятор
pytest Tests/Calc_test.py --alluredir=allure-results

# только магазин
pytest Tests/Shop_test.py --alluredir=allure-results

# посмотреть отчёт
allure serve allure-results
