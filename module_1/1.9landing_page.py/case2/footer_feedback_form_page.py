# footer_feedback_form_page.py
from selenium.webdriver.common.by import By

from base_page import BasePage


class FooterFeedbackFormPage(BasePage):
    SEARCH_INPUT = (By.ID, "footer-search")

    def fill_form(self, name, email, message):
        name_input = self.wait_for_element(self.SEARCH_INPUT)
        name_input.send_keys(name)

        email_input = self.driver.find_element(By.ID, "footer-email")
        email_input.send_keys(email)

        message_input = self.driver.find_element(By.ID, "footer-message")
        message_input.send_keys(message)

        submit_button = self.driver.find_element(By.ID, "footer-submit")
        submit_button.click()
