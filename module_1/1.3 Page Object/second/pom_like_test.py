from selenium.webdriver.common.by import By


class Cart(object):
    url = "http://pizzeria.skillbox.cc/cart/"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.url)
        return self

    def click_checkout_button(self):
        checkout_button = self.driver.find_element(
            By.CLASS_NAME, "checkout-button.button.alt.wc-forward"
        )
        checkout_button.click()
        return Checkout(self.driver)

    def is_opened(self):
        return "/card/" in self.driver.current_url


class Checkout(object):
    uri = "/checkout/"

    def __init__(self, driver):
        self.driver = driver

    def is_opened(self):
        return self.uri in self.driver.current_url


def test_checkout_button(driver, login):
    # arrange
    cart = Cart(driver)
    cart.open()
    # act
    checkout = cart.click_checkout_button()
    # assert
    assert checkout.is_opened()
