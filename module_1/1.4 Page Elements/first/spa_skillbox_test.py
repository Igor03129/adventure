from selenium.webdriver.common.by import By


class Landing(object):
    CALLBACK_BUTTON = (By.XPATH, "//div[@class='catalog']//button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://skillbox.ru/")
        return self

    def click_callback_submit(self):
        callback_button = self.driver.find_element(*self.CALLBACK_BUTTON)
        callback_button.click()
        return self

    def is_opened(self):
        return "https://skillbox.ru/" == self.driver.current_url


def test_callback_button_empty_click(driver):
    # arrange
    landing = Landing(driver)
    # act
    landing.open().click_callback_submit()
    # assert
    assert landing.is_opened()
