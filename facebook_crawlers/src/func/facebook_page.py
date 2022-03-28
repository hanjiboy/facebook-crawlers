import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from facebook_crawlers.config.config import TestData
from facebook_crawlers.src.func.basepage import BasePage


class FacebookPageAttrs(BasePage):
    USER_EMAIL = (By.ID, 'email')

    USER_PASSWORD = (By.ID, 'pass')

    LOGIN_BUTTON = (By.NAME, 'login')

    LOGIN_BLOCK = (By.XPATH, '//div[@class="_6luv _52jv"]')

    GROUP_TEXT = (By.XPATH, '//h1[@dir="auto"]')

    LINK_XPATH = (By.XPATH, '//div[@class="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"]'
                            '//a[@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9'
                            ' nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9'
                            ' a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]')
    # Link location.

    EXPAND_XPATH = (By.XPATH, '//div[@role="button"]'
                              '//span[@class="j83agx80 fv0vnmcu hpfvmrgz"]'
                              '//span[@dir="auto"]')  # Expand location.

    ARTICLE_TITLE_XPATH = (By.XPATH, '//div[@class="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"]'
                                     '//div[@dir="auto"]')  # Article title location.

    ARTICLE_NAME_BOXES_XPATH = (By.XPATH, '//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]'
                                          '//a[@role="link"]//span[@class="pq6dq46d"]'
                                          '//span[@dir="auto"]')  # Article message username location.

    ARTICLE_CONTENT_BOXES_XPATH = (By.XPATH, '//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]'
                                             '//div[@class="ecm0bbzt e5nlhep0 a8c37x1j"]'
                                             '//div[@class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]')
    # Article message content location.

    def __init__(self, driver):
        super().__init__(driver)

    def get_login_block_exist(self):
        self.driver.get(TestData.LOGIN_URL)
        return self.is_visible(self.LOGIN_BLOCK)

    def get_login_page_title(self, title):
        return self.get_title(title)

    def do_login(self, username, password):
        self.send_keys(self.USER_EMAIL, username)
        self.send_keys(self.USER_PASSWORD, password)
        self.something_click(self.LOGIN_BUTTON)

    def get_group_page_title(self):
        time.sleep(2)
        self.driver.get(TestData.GROUP_URL)
        return self.get_element_text(self.GROUP_TEXT)

    def get_article_link(self):
        links = []
        self.is_scroll(1)
        posts = self.get_elements(self.LINK_XPATH)
        for post in posts:
            ActionChains(self.driver).move_to_element(post).perform()
            links.append(post.get_attribute('href').split('?', 1)[0])
        return links

    def click_expand_button(self):
        if self.get_elements(self.EXPAND_XPATH):
            self.something_click(self.EXPAND_XPATH)
            return '點到了'

    def get_article_title(self):
        return self.is_visible(self.ARTICLE_TITLE_XPATH)

    def get_article_message_name_boxes(self):
        return self.is_visible(self.ARTICLE_NAME_BOXES_XPATH)

    def get_article_message_content_boxes(self):
        return self.is_visible(self.ARTICLE_CONTENT_BOXES_XPATH)

    def get_data(self):
        response = self.mongo_data()
        return response
