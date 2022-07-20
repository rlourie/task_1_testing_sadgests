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

    @staticmethod
    def check_all_suggests():
        pass

    def test_case_1(self):
        counter = 0
        self.driver.get(self.url)
        search_form = self.driver.find_element(By.NAME, 'q')
        search_form.click()
        count_suggest = len(self.driver.find_elements(By.CLASS_NAME, "DesktopSuggests-suggest"))
        self.driver.get(self.url)
        for i in range(1, count_suggest + 1):
            x_path_suggest = f"//ul[@class='DesktopSuggests-suggestsListWrapper MainPageContainer-suggestsListWrapper DesktopSuggests-keyboardUnControl']/li[{i}]"
            search_form = self.driver.find_element(By.NAME, 'q')
            search_form.click()
            current_suggest = self.driver.find_element(By.XPATH, x_path_suggest)
            curent_text = current_suggest.text
            current_suggest.click()
            fact_text = self.driver.find_element(By.NAME, 'q')
            value = fact_text.get_dom_attribute('value')
            if value == curent_text:
                counter += 1
            self.driver.get(self.url)
        self.driver.quit()
        assert counter == 10


print(Test.translate_ru('Ghbdtn vbh'))
print(Test.translate_en('Руддщ цщкдв'))
