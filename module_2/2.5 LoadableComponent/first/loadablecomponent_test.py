from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory.Pagefactory import PageFactory, ElementNotFoundException

from urllib.parse import urlparse

from abc import ABC, abstractmethod


class LoadableComponent(ABC):
    def __init__(self, driver):
        self.driver = driver

    def get(self):
        self.load()
        self.is_loaded()
        return self

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def is_loaded(self):
        pass


class LandingPageFactory(PageFactory, LoadableComponent):
    SEARCH_SUGGESTS = (By.XPATH, "//div[@class='ui-select-popup']//li")

    URL = "https://skillbox.ru/"

    locators = {
        "header_button": (
            By.XPATH,
            "//header//button[contains(@class, 'toggle-menu')]",
        ),
        "input": (By.XPATH, "//header//input[@name='search']"),
    }

    def __init__(self, driver):
        self.driver = driver
        self.highlight = True

    def load(self):
        self.driver.get(self.URL)
        return self

    def open_menu(self):
        self.header_button.click()
        return self

    def search_input(self, search_text: str):
        self.open_menu()
        try:
            self.input.send_keys(search_text)
        except ElementNotFoundException:
            self.open_menu()
            self.input.send_keys(search_text)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_SUGGESTS)
        )
        suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTS)
        return [suggestion.text for suggestion in suggestions]

    def is_loaded(self):
        return self.URL == self.driver.current_url

        """someone threats static methods are evil"""
        parts = urlparse(url)
        return parts.scheme, parts.netloc, parts.path


def test_whereis_loadable(driver):
    """code from 1.6"""
    # arrange
    search = "Тест"
    landing = LandingPageFactory(driver)
    # act
    landing.get().open_menu()
    suggestions = landing.search_input(search)

    # assert
    assert all(
        search.lower() in suggestion.lower() for suggestion in suggestions
    ), f"Not all suggestion texts contain '{search}'"
