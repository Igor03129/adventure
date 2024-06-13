# Файл test_search.py
import unittest
from selenium import webdriver
from landing_page import LandingPage
#from search_result_detail_page import SearchResultDetailPage
from urllib.parse import unquote

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://skillbox.ru")

    def test_relevant_search_results(self):
        landing_page = LandingPage(self.driver)
        search_results_page = landing_page.search("тестирование")
        results = search_results_page.get_search_results()
        for result in results:
            self.assertIn("тестирование", result.text.lower())

    def test_navigation_from_search_result(self):
        landing_page = LandingPage(self.driver)
        search_results_page = landing_page.search("тестирование")
        result_detail_page = search_results_page.click_search_result(0)
        url = result_detail_page.get_url()
        decoded_url = unquote(url)
        self.assertIn("тестирование", decoded_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
