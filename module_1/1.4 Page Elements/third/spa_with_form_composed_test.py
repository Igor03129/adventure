from selenium.webdriver.common.by import By


class CallbackForm(object):
    CALLBACK_FORM = (By.XPATH, "//section[@class='catalog-form']")
    CALLBACK_BUTTON = (By.XPATH, "//div[@class='catalog']//button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.form = self.driver.find_element(*self.CALLBACK_FORM)
        self.form.location_once_scrolled_into_view
        return self

    def click_callback_submit(self):
        callback_button = self.driver.find_element(*self.CALLBACK_BUTTON)
        callback_button.click()
        return self

    def is_opened(self):
        return self.form.is_displayed()


class Landing(object):
    def __init__(self, driver):
        self.driver = driver
        self.callback_form = CallbackForm(driver)

    def open(self):
        self.driver.get("https://skillbox.ru/")
        return self

    def is_opened(self):
        return "https://skillbox.ru/" == self.driver.current_url


def test_callback_button_empty_click(driver):
    # arrange
    landing = Landing(driver)
    landing.open()

    # act
    landing.callback_form.open().click_callback_submit()

    # assert
    assert landing.is_opened()
    assert landing.callback_form.is_opened()
