from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LandingPageFactory(object):
    HEADER_BUTTON = (By.XPATH, "//header//button[contains(@class, 'toggle-menu')]")
    HEADER_INPUT = (By.XPATH, "//header//input[@name='search']")
    SEARCH_SUGGESTS = (By.XPATH, "//div[@class='ui-select-popup']//li")

    URL = "https://skillbox.ru/"

    def __init__(self, driver):
        self.driver = driver

    @property
    def header_button(self):
        return WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.HEADER_BUTTON)
        )

    @property
    def input(self):
        return WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.HEADER_INPUT)
        )

    def open(self):
        self.driver.get(self.URL)
        return self

    def open_menu(self):
        self.header_button.click()
        return self

    def search_input(self, search_text: str):
        self.open_menu()
        try:
            self.input.send_keys(search_text)
        except TimeoutException:
            self.open_menu()
            self.input.send_keys(search_text)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_SUGGESTS)
        )
        suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTS)
        return [suggestion.text for suggestion in suggestions]

    def is_opened(self):
        return self.URL == self.driver.current_url


def test_whereismenu_brew(driver):
    """code from module 1"""
    # arrange
    search = "Тест"
    landing = LandingPageFactory(driver)
    # act
    landing.open().open_menu()
    suggestions = landing.search_input(search)

    # assert
    assert all(
        search.lower() in suggestion.lower() for suggestion in suggestions
    ), f"Not all suggestion texts contain '{search}'"
