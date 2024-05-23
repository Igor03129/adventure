import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


options = Options()
# options.add_argument("--headless")
options.add_argument("window-size=1600,1400")


@pytest.fixture(scope="module", autouse=True)
def driver():
    # Instantiate the WebDriver (in this case, using Chrome)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    yield driver
    # Close the WebDriver
    driver.quit()
