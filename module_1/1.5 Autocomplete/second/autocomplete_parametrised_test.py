import pytest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, s
        )

    original_style = element.get_attribute("style")
    apply_style("border: 10px solid red;")
    time.sleep(3)
    apply_style(original_style)


class Landing(object):
    """ """

    SEARCH_INPUT = (By.XPATH, "//input[@name='search']")
    SEARCH_FORM = (By.CLASS_NAME, "ui-search-desktop")
    SEARCH_SUGGESTS = (By.XPATH, "//div[@class='ui-select-popup']//li")
    URL = "https://skillbox.ru/"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def goto_search_form(self):
        search_form = self.driver.find_element(*self.SEARCH_FORM)
        search_form.location_once_scrolled_into_view
        return self

    def search_profession(self, search_text: str):
        """
        :param search_text: text to search
        also window.scrollTo is a hack to make form fully visible to demonstrate highlight
        """
        input = self.driver.find_element(*self.SEARCH_INPUT)
        input.location_once_scrolled_into_view
        self.driver.execute_script("window.scrollTo(0, 400);")
        highlight(input)
        input.send_keys(search_text)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_SUGGESTS)
        )
        suggestions = self.driver.find_elements(*self.SEARCH_SUGGESTS)
        return [suggestion.text for suggestion in suggestions]

    def is_opened(self):
        return self.URL == self.driver.current_url


@pytest.mark.parametrize("search", ["Автотесты", "Python"])
def test_suggest_is_related(driver, search):
    # arrange
    landing = Landing(driver)
    # act
    suggestion_texts = landing.open().search_profession(search)
    # assert
    assert all(
        search in suggestion_text for suggestion_text in suggestion_texts
    ), f"Not all suggestion texts contain '{search}'"
