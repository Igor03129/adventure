from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

from typing import List, Tuple
from urllib.parse import urlparse
import pytest
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


class Landing(object):
    """represents generic course page"""

    URL: str

    def __init__(self, driver, url):
        self.driver = driver
        self.URL = url

        self.ribbon = RibbonWidget(self.driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    def is_opened(self):
        return (
            self._get_base_url(self.URL).path
            == self._get_base_url(self.driver.current_url).path
        )

    @staticmethod
    def _get_base_url(url):
        """someone threats static methods are evil"""
        parts = urlparse(url)
        return parts


class CoursesNavigationWidget:
    BUTTONS = (By.XPATH, '//div[@class="courses-page__header"]//a')

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def _get_buttons(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.BUTTONS)
        )

    def _is_button_active(self, button):
        return "ui-tab--active" in button.get_attribute("class")

    def get_active_button_url(self):
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.get_attribute("href")

        raise CoursesButtonNotFound("No active button found")

    def get_active_button_text(self):
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.text.strip()

        raise CoursesButtonNotFound("No active button found")


class CoursesButtonNotFound(Exception):
    def __init__(self, message="No button found"):
        self.message = message
        super().__init__(self.message)


class CoursePage(object):
    """"represents generic course page""" ""

    URL: str

    def __init__(self, driver, url):
        self.driver = driver
        self.URL = url

        self.navigation = CoursesNavigationWidget(self.driver)
        self.courses = CoursesTilesWidget(self.driver)
        self.professions = ProfessionsTilesWidget(self.driver)
        self.ribbon = RibbonWidget(self.driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    @staticmethod
    def _get_base_url(url):
        """"someone threats static methods are evil""" ""
        parts = urlparse(url)
        return parts

    def is_opened(self):
        return (
            self._get_base_url(self.URL).path
            == self._get_base_url(self.driver.current_url).path
        ) and self.courses.is_loaded()


class TilesWidget:
    PATH: Tuple[str, str]
    TILES: Tuple[str, str]

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def is_loaded(self):
        """"but maybe page is not loaded?""" ""
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


class RibbonWidget:
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

    def is_displayed(self):
        try:
            element = self.driver.find_element(*self.PATH)
            return element.is_displayed()
        except NoSuchElementException:
            return False


def test_button_is_active(driver):
    # arrange
    about = "https://skillbox.ru/code/"
    # text = 'Программирование'
    course = CoursePage(driver, about)
    # act
    course.open()
    selected_button_url = course.navigation.get_active_button_url()
    # assert
    assert course.is_opened()
    assert selected_button_url in course.URL


@pytest.mark.parametrize(
    "about, text",
    [
        ("https://skillbox.ru/code/", "Программирование"),
        ("https://skillbox.ru/english/", "Английский язык")
        # additional parameter sets can be added here
    ],
)
def test_button_is_active_all(driver, about: str, text: str):
    # arrange
    course = CoursePage(driver, about)
    # act
    course.open()
    selected_button_url = course.navigation.get_active_button_url()
    selected_button_text = course.navigation.get_active_button_text()
    # assert
    assert course.is_opened()
    assert selected_button_url in course.URL
    assert selected_button_text == text


@pytest.mark.parametrize(
    "about, is_courses, is_professions",
    [
        ("https://skillbox.ru/code/", True, True),
        ("https://skillbox.ru/english/", True, False)
        # additional parameter sets can be added here
    ],
)
def test_sections_are_on_page(
    driver, about: str, is_courses: bool, is_professions: bool
):
    # arrange
    course = CoursePage(driver, about)
    # act
    course.open()
    # assert
    assert course.courses.is_loaded() == is_courses
    assert course.professions.is_loaded() == is_professions


@pytest.mark.parametrize(
    "about, page",
    [
        ("https://skillbox.ru/", Landing),
        ("https://skillbox.ru/english/", CoursePage)
        # additional parameter sets can be added here
    ],
)
def test_sections_are_on_page(driver, about, page):
    # arrange
    SUT = page(driver, about)
    # act
    SUT.open()
    SUT.ribbon.open()

    # assert
    assert SUT.ribbon.is_displayed()
