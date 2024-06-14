from module_1.fixtures.driver import driver


URL = "https://skillbox.ru/"
email_place = "input.ui-field__input.f.f--16"

class Landing(object, driver):



    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def open_menu(self):
        header_button = self.driver.find_element(*self.email_place)
        header_button.click()
        return self

    def search_input(self, search_text: str):
        self.open_menu()
        self.input.send_keys(search_text)
        return self

    def test_whereismenu(driver):
        # arrange
        search = "Тест"
        landing = Landing(driver)
        # act
        suggestion_texts = landing.open().open_menu_input()
        landing.search_input(search)

