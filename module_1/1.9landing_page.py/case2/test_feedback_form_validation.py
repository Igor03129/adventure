# test_feedback_form_validation.py

import unittest
from selenium import webdriver
from pages.landing_page import LandingPage
from utils.test_data import VALID_NAME, INVALID_EMAIL, VALID_MESSAGE

class TestFeedbackFormValidation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://skillbox.ru")
        self.landing_page = LandingPage(self.driver)

    def test_invalid_email_validation(self):
        feedback_form = self.landing_page.feedback_form
        feedback_form.fill_form(VALID_NAME, INVALID_EMAIL, VALID_MESSAGE)
        # Проверка наличия и текста ошибки в случае неверного email

    def test_valid_submission(self):
        feedback_form = self.landing_page.feedback_form
        feedback_form.fill_form(VALID_NAME, VALID_EMAIL, VALID_MESSAGE)
        # Проверка успешной отправки валидной формы

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
