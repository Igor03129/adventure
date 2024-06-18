from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple, Union
from urllib.parse import urlparse
import pytest
from selenium.common.exceptions import NoSuchElementException
import time


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


class CoursesButtonNotFound(Exception):
    def __init__(self, message="No button found"):
        self.message = message
        super().__init__(self.message)


class CoursesNavigationWidget:
    BUTTONS: Tuple[str, str] = (By.XPATH, '//div[@class="courses-page__header"]//a')

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

    def _get_buttons(self) -> List[WebElement]:
        """it is a private method"""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.BUTTONS)
        )

    def click_course_button(self, text: str) -> None:
        buttons = self._get_buttons()
        for button in buttons:
            if button.text == text:
                button.click()
                return

        raise CoursesButtonNotFound(f"No button found with the text '{text}'")

    def _is_button_active(self, button: WebElement) -> bool:
        """private method too"""
        return "ui-tab--active" in button.get_attribute("class")

    def get_active_button_url(self) -> str:
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.get_attribute("href")

        raise CoursesButtonNotFound("No active button found")

    def get_active_button_text(self) -> str:
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.text.replace("\n", "").strip()

        raise CoursesButtonNotFound("No active button found")

    def is_loaded(self):
        try:
            self._get_buttons()
            return True
        except WebDriverException:
            return False


class TilesWidget:
    PATH: Tuple[str, str]
    TILES: Tuple[str, str]

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

    def is_loaded(self) -> bool:
        """but maybe page is not loaded?"""
        try:
            self.driver.find_element(*self.PATH)
            return True
        except NoSuchElementException:
            return False


class ProfessionsTilesWidget(TilesWidget):
    PATH: Tuple[str, str] = (
        By.XPATH,
        '//div[@class="courses-section"]//section//h2[contains(text(), "Профессии")]',
    )


class CoursesTilesWidget(TilesWidget):
    PATH: Tuple[str, str] = (
        By.XPATH,
        '//div[@class="courses-section"]//section//h2[contains(text(), "Курсы")]',
    )


class CoursesRibbonWidget:
    PATH: Tuple[str, str] = (
        By.XPATH,
        '//div[@data-algorithm="popular" and @data-widget-applied="true"]',
    )

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver

    def open(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PATH)
        )
        element.location_once_scrolled_into_view
        highlight(element)

        return self

    def is_displayed(self) -> bool:
        try:
            element = self.driver.find_element(*self.PATH)
            return element.is_displayed()
        except NoSuchElementException:
            return False


class CoursePage(object):
    """represents generic course page"""

    URL: str

    def __init__(self, driver, url):
        self.driver = driver
        self.URL = url
        self.navigation = CoursesNavigationWidget(driver)

        self.professions = ProfessionsTilesWidget(driver)
        self.courses = CoursesTilesWidget(driver)

        self.ribbon = CoursesRibbonWidget(driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    def is_opened(self):
        return (
            self._get_base_url(self.URL) == self._get_base_url(self.driver.current_url)
            and self.courses.is_loaded()
        )

    @staticmethod
    def _get_base_url(url):
        """someone threats static methods are evil"""
        parts = urlparse(url)
        return parts.scheme, parts.netloc, parts.path


class Landing(object):
    """represents generic course page"""

    URL: str

    def __init__(self, driver, url):
        self.driver = driver
        self.URL = url

        self.ribbon = CoursesRibbonWidget(driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    def is_opened(self):
        return self._get_base_url(self.URL) == self._get_base_url(
            self.driver.current_url
        )

    @staticmethod
    def _get_base_url(url):
        """someone threats static methods are evil"""
        parts = urlparse(url)
        return parts.scheme, parts.netloc, parts.path


@pytest.mark.parametrize(
    "about, page",
    [
        ("https://skillbox.ru/", Landing),
        ("https://skillbox.ru/english/", CoursePage)
        # additional parameter sets can be added here
    ],
)
def test_sections_are_on_page(driver, about: str, page: Union[Landing, CoursePage]):
    # arrange
    SUT = page(driver, about)
    # act
    SUT.open()
    SUT.ribbon.open()

    # assert
    assert SUT.ribbon.is_displayed()
