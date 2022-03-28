import time
import pymongo

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['Gamesofa Careers']
        self.collections = db['ArticleList']

    def something_click(self, by_locator):
        self.wait.until(EC.visibility_of_element_located(by_locator)).click()

    def send_keys(self, by_locator, value):
        self.wait.until(EC.visibility_of_element_located(by_locator)).send_keys(value)

    def get_element_text(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.text

    def get_elements(self, by_locator):
        elements = self.wait.until(EC.visibility_of_all_elements_located(by_locator))
        return elements

    def get_title(self, title):
        self.wait.until(EC.title_is(title))
        return self.driver.title

    def is_visible(self, by_locator):
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def is_scroll(self, limit):
        for _ in range(int(limit) - 1):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)

    def mongo_data(self):
        return self.collections.find_one()
