from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class BaseInputElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator)
        )
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, *args):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class FormNameElement(BaseInputElement):
    locator = (By.XPATH, "//section[@class='catalog-form']//input[@name='name']")


class FormPhoneElement(BaseInputElement):
    locator = (By.XPATH, "//section[@class='catalog-form']//input[@name='phone']")


class FormEmailElement(BaseInputElement):
    locator = (By.XPATH, "//section[@class='catalog-form']//input[@name='email']")


class CallbackForm(object):
    name = FormNameElement()
    phone = FormPhoneElement()
    email = FormEmailElement()
    CALLBACK_FORM = (By.XPATH, "//section[@class='catalog-form']")

    def __init__(self, driver):
        self.driver = driver

    def enter_name(self, query):
        self.name = [query, Keys.RETURN]

    def enter_phone(self, query):
        self.phone = [query, Keys.RETURN]

    def enter_email(self, query):
        self.email = [query, Keys.RETURN]

    def is_sent(self):
        expected_text = (
            "Спасибо за заявку! Наш консультант перезвонит вам в течение часа."
        )

        try:
            return WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(self.CALLBACK_FORM, expected_text)
            )
        except TimeoutException:
            return False


class Landing(object):
    def __init__(self, driver):
        self.driver = driver
        self.callback_form = CallbackForm(driver)

    def open(self):
        self.driver.get("https://skillbox.ru/")
        return self

    def is_opened(self):
        return "https://skillbox.ru/" == self.driver.current_url


def test_callback_button_add_values(driver):
    # arrange
    landing = Landing(driver)
    landing.open()

    # act
    landing.callback_form.enter_name("test")
    landing.callback_form.enter_phone("+79260001234")
    landing.callback_form.enter_email("test@test.org")

    # assert
    assert landing.is_opened()
    assert landing.callback_form.is_sent()
