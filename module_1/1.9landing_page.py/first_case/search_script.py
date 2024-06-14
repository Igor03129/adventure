from module_1.fixtures.driver import driver

button = "svg.ui-tab__media.ui-tab__media--icon.icon.sprite-icons"
search_object = "//*[text()='Аналитика']"
URL = "https://skillbox.ru/"

class Landing(object, driver):


    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def button_click(self):
        return self.button_click(button).click()

    def button_is_displayed(self):
        return self.button().is_displayed()

    def search_result(self):
        return self.search_result(search_object).is_displayed()

