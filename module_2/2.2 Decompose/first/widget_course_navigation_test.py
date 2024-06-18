from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import pytest


# находим на странице локатор
class CoursesNavigationWidget:
    BUTTONS = (By.XPATH, '//div[@class="courses-page__header"]//a')

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def _get_buttons(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.BUTTONS)
        )

    # получили кнопки

    # дописываем остальные методы

    def click_course_button(self, text):  # TODO return another PO from here
        buttons = self._get_buttons()
        for button in buttons:
            if button.text == text:
                button.click()
                return

        raise Exception(f"No button found with the text '{text}'")

    # как понять, что кнопка активна? подсмотрим в код страницы

    def _is_button_active(self, button):
        return "ui-tab--active" in button.get_attribute("class")

    def get_active_button_url(self):
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.get_attribute("href")

        raise Exception("No active button found")

    def get_active_button_text(self):
        buttons = self._get_buttons()
        for button in buttons:
            if self._is_button_active(button):
                return button.text.replace("\n", "").strip()

        raise Exception("No active button found")


# все исключения странные, напишем свое - поправим выше исключения


class CoursesButtonNotFound(Exception):
    def __init__(self, message="No button found"):
        self.message = message
        super().__init__(self.message)


# пишем дальше страницу
# одна и та же для всех курсов - может быть такое, что разные страницы один по,
# обратите на это внимание


class CoursePage(object):
    """represents generic course page"""

    URL: str

    def __init__(self, driver, url):
        self.driver = driver
        self.URL = url
        self.navigation = CoursesNavigationWidget(driver)

    def open(self):
        self.driver.get(self.URL)
        return self

    # напишем проверку честнее - посмотрим в браузере на урл - из чего он состоит
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
