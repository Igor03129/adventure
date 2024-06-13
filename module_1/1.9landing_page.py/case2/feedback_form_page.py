# feedback_form_page.py
from selenium.webdriver.common.by import By

from base_page import BasePage


class FeedbackFormPage(BasePage):
    SEARCH_INPUT = (By.ID, "search")
    SUBMIT_BUTTON = (By.ID, "submit")

    def fill_form(self, name, email, message):
        name_input = self.wait_for_element(self.SEARCH_INPUT)
        name_input.send_keys(name)

        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys(email)

        message_input = self.driver.find_element(By.ID, "message")
        message_input.send_keys(message)

        submit_button = self.driver.find_element(self.SUBMIT_BUTTON)
        submit_button.click()
