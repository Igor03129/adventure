# Файл landing_page.py
class LandingPage:
    def __init__(self, driver):
        self.driver = driver

    def search(self, keyword):
        search_input = self.driver.find_element_by_id("search")
        search_input.send_keys(keyword)
        search_input.submit()
        return SearchResultsPage(self.driver)


# Файл search_results_page.py
class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver

    def get_search_results(self):
        results = self.driver.find_elements_by_class_name("search-result")
        return results

    def click_search_result(self, index):
        results = self.get_search_results()
        results[index].click()
        return SearchResultDetailPage(self.driver)


# Файл search_result_detail_page.py
class SearchResultDetailPage:
    def __init__(self, driver):
        self.driver = driver

    def get_url(self):
        return self.driver.current_url
