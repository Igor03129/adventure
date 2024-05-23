from locators import CHECKOUT_BUTTON


def test_checkout_button(driver, login):
    # arrange
    driver.get("http://pizzeria.skillbox.cc/cart/")
    button = driver.find_element(*CHECKOUT_BUTTON)

    # act
    button.click()

    # assert
    assert driver.current_url == "http://pizzeria.skillbox.cc/checkout/"
