import pytest


@pytest.fixture(scope="module", autouse=False)
def login(driver):
    # Navigate to the webpage
    driver.get("http://pizzeria.skillbox.cc/")

    # Add the cookies to the local storage
    cookies = [
        {
            "name": "wordpress_608a4400240853029106aa1f2d8f9149",
            "value": "Python_877_dnd%7C1687892991%7CaHviUUEZv70OC8MtnUpCWQnNUjjvgnLTWbKt2ueCtzh%7C628d3e4a5667dd3c22f8839580c088ee80d7bcdc1ae04eb122a290676e3c309b",
            "domain": "pizzeria.skillbox.cc",
        },
        {
            "name": "wordpress_logged_in_608a4400240853029106aa1f2d8f9149",
            "value": "Python_877_dnd%7C1687892991%7CaHviUUEZv70OC8MtnUpCWQnNUjjvgnLTWbKt2ueCtzh%7Cc2df50e4eb17835f7224dd0cdec308d95ded8f0a7f21b059103b29de281fc9f0",
            "domain": "pizzeria.skillbox.cc",
        },
    ]
    for cookie in cookies:
        driver.add_cookie(cookie)
