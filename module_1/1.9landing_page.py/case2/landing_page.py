# landing_page.py

from base_page import BasePage
from feedback_form_page import FeedbackFormPage
from footer_feedback_form_page import FooterFeedbackFormPage

class LandingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://skillbox.ru")
        self.feedback_form = FeedbackFormPage(driver)
        self.footer_feedback_form = FooterFeedbackFormPage(driver)
