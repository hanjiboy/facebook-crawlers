import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from facebook_crawlers.config.config import TestData


@pytest.fixture(scope='class', autouse=True)
def browser(request):
    CHROMEDRIVER = Service(TestData.DRIVER_PATH)
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'excludeSwitches': ['enable-logging'],
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(service=CHROMEDRIVER, options=options)
    driver.maximize_window()
    request.cls.driver = driver
    yield driver
    driver.close()
