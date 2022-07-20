# Тестирование саджестов.

Для запуска локально

```
pytest tests
```

## Для создания allure отчета

```
pytest --alluredir results
allure serve results
```

## Для тестирования поисковой строки по другим категориям

Нужно изменить `self.url = "https://go.mail.ru/` в файле `test_pytest.py`  на адресс тестируемого раздела, например
на `https://go.mail.ru/search_social?fr=main&frm=main`
