# test_feedback_form_navigation.py

import unittest
from selenium import webdriver
from pages.landing_page import LandingPage
from utils.test_data import VALID_NAME, VALID_EMAIL, VALID_MESSAGE

class TestFeedbackFormNavigation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://skillbox.ru")
        self.landing_page = LandingPage(self.driver)

    def test_invalid_submission_navigation(self):
        feedback_form = self.landing_page.feedback_form
        feedback_form.fill_form(VALID_NAME, INVALID_EMAIL, VALID_MESSAGE)
        # Проверка отсутствия перехода после отправки невалидной формы

    def test_valid_submission_navigation(self):
        feedback_form = self.landing_page.feedback_form
        feedback_form.fill_form(VALID_NAME, VALID_EMAIL, VALID_MESSAGE)
        # Проверка перехода после отправки валидной формы

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
