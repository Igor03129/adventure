import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BaseDropdownElement(object):
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator)
        )
        select_element = Select(driver.find_element(*self.locator))
        select_element.select_by_visible_text(value)
        return select_element

    def __get__(self, obj, *args):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator)
        )
        select_element = Select(driver.find_element(*self.locator))
        return [option.text for option in select_element.options]


class DropdownFirstElement(BaseDropdownElement):
    locator = (By.CSS_SELECTOR, "[id*='select-1']")


class DropdownSecondElement(BaseDropdownElement):
    locator = (By.CSS_SELECTOR, "[id*='select-2']")


class DropdownThirdElement(BaseDropdownElement):
    locator = (By.CSS_SELECTOR, "[id*='select-3']")


class DropdownsPage(object):
    URL = "https://s.xhtml.ru/embed/?src=R5Mb4"
    first = DropdownFirstElement()
    second = DropdownSecondElement()
    third = DropdownThirdElement()

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self


def test_dropdown_is_related(driver):
    # arrange
    page = DropdownsPage(driver)
    # act
    page.open()
    page.first = "A"
    # assert
    assert "A-A" in page.second, "Option A-A is not available in next dropdown"
    assert "B-A" not in page.second, "Option B-A should not be in next dropdown"
