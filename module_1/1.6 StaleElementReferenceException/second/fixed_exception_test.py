from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class Landing(object):
    HEADER_BUTTON = (By.XPATH, "//header//button[contains(@class, 'toggle-menu')]")
    HEADER_INPUT = (By.XPATH, "//header//input[@name='search']")
    SEARCH_SUGGESTS = (By.XPATH, "//div[@class='ui-select-popup']//li")

    URL = "https://skillbox.ru/"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def open_menu(self):
        header_button = self.driver.find_element(*self.HEADER_BUTTON)
        header_button.click()
        return self

    def open_menu_input(self):
        self.open_menu()
        input = self.driver.find_element(*self.HEADER_INPUT)
        self.input = input

    def search_input(self, search_text: str):
        self.open_menu()
        try:
            self.input.send_keys(search_text)
        except StaleElementReferenceException:
            self.open_menu_input()
            self.input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.HEADER_INPUT)
            )

            self.input.send_keys(search_text)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_SUGGESTS)
        )
        suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTS)
        return [suggestion.text for suggestion in suggestions]

    def is_opened(self):
        return self.URL == self.driver.current_url


def test_whereismenu(driver):
    # arrange
    search = "Тест"
    landing = Landing(driver)
    # act
    landing.open().open_menu_input()
    suggestions = landing.search_input(search)

    # assert
    assert all(
        search.lower() in suggestion.lower() for suggestion in suggestions
    ), f"Not all suggestion texts contain '{search}'"
