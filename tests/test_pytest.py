import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class Test:
    def setup(self):
        self.url = "https://go.mail.ru/"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    @staticmethod
    def translate_ru(value_str):
        layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                   'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                          "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                          'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        return (value_str.translate(layout))

    @staticmethod
    def translate_en(value_str):
        layout = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                   'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                          "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                          'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))
        return (value_str.translate(layout))

    def check_all_request_suggests(self, text):
        counter = 0
        self.driver.get(self.url)
        search_form = self.driver.find_element(By.NAME, 'q')
        search_form.click()
        search_form.send_keys(text)
        count_suggest = len(self.driver.find_elements(By.CLASS_NAME, "DesktopSuggests-suggest"))
        self.driver.get(self.url)
        for i in range(1, count_suggest + 1):
            x_path_suggest = f"//ul[@class='DesktopSuggests-suggestsListWrapper MainPageContainer-suggestsListWrapper DesktopSuggests-keyboardUnControl']/li[{i}]"
            search_form = self.driver.find_element(By.NAME, 'q')
            search_form.click()
            search_form.send_keys(text)
            current_suggest = self.driver.find_element(By.XPATH, x_path_suggest)
            curent_text = current_suggest.text
            current_suggest.click()
            fact_text = self.driver.find_element(By.NAME, 'q')
            value = fact_text.get_dom_attribute('value')
            if value == curent_text:
                counter += 1
            self.driver.get(self.url)
        self.driver.quit()
        return counter, count_suggest

    def check_all_in_suggests(self, text, ru_1_en_2=0):
        counter = 0
        self.driver.get(self.url)
        search_form = self.driver.find_element(By.NAME, 'q')
        search_form.click()
        search_form.send_keys(text)
        count_suggest = len(self.driver.find_elements(By.CLASS_NAME, "DesktopSuggests-suggest"))
        for i in range(1, count_suggest + 1):
            x_path_suggest = f"//ul[@class='DesktopSuggests-suggestsListWrapper MainPageContainer-suggestsListWrapper DesktopSuggests-keyboardUnControl']/li[{i}]"
            current_suggest = self.driver.find_element(By.XPATH, x_path_suggest)
            current_text = current_suggest.text
            if ru_1_en_2 == 0:
                if text in current_text:
                    counter += 1
            else:
                if ru_1_en_2 == 1:
                    if Test.translate_ru(text) in current_text:
                        counter += 1
                if ru_1_en_2 == 2:
                    if Test.translate_en(text) in current_text:
                        counter += 1
        self.driver.quit()
        return counter, count_suggest

    # Тесты на запросы с саджестов.
    def test_case_1(self):
        a, b = Test.check_all_request_suggests(self, 'тест')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_2(self):
        a, b = Test.check_all_request_suggests(self, 'test')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_3(self):
        a, b = Test.check_all_request_suggests(self, '')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_4(self):
        a, b = Test.check_all_request_suggests(self, '~')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_5(self):
        a, b = Test.check_all_request_suggests(self, '1234')
        assert ((a == b) and (a != 0 and b != 0))

    # Тесты на вхождение запроса в саджест односложные.
    def test_case_6(self):
        a, b = Test.check_all_in_suggests(self, 'тест')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_7(self):
        a, b = Test.check_all_in_suggests(self, 'test')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_8(self):
        a, b = Test.check_all_in_suggests(self, '*')
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_9(self):
        a, b = Test.check_all_in_suggests(self, '1234')
        assert ((a == b) and (a != 0 and b != 0))

    # Тесты на вхождние транслитирации односложные.
    def test_case_10(self):
        a, b = Test.check_all_in_suggests(self, 'еуые', 2)
        assert ((a == b) and (a != 0 and b != 0))

    def test_case_11(self):
        a, b = Test.check_all_in_suggests(self, 'ntcn', 1)
        assert ((a == b) and (a != 0 and b != 0))

    # Тест на некоректные данные для саджеста
    def test_case_12(self):
        a, b = Test.check_all_in_suggests(self, 'rfgthygjh')
        assert (a == 0 and b == 0)

    def test_case_13(self):
        a, b = Test.check_all_in_suggests(self, 'акперинго')
        assert (a == 0 and b == 0)
