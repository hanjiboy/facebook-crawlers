import os
import pytest

from dotenv import load_dotenv

from facebook_crawlers.config.config import TestData
from facebook_crawlers.src.func.facebook_page import FacebookPageAttrs

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')


@pytest.mark.usefixtures('browser')
class BaseTest:
    pass


@pytest.fixture(scope='module', autouse=True)
def log():
    print('\n------initiating chrome driver------')
    yield
    print('\n------teardown------')


class TestCrawlerPage(BaseTest):
    def test_login_block_exist(self, log):
        self.crawler = FacebookPageAttrs(self.driver)
        frame = self.crawler.get_login_block_exist()
        assert frame is True

    def test_login_page_title(self):
        self.crawler = FacebookPageAttrs(self.driver)
        title = self.crawler.get_title(TestData.LOGIN_PAGE_TITLE)
        assert TestData.LOGIN_PAGE_TITLE in title

    def test_login(self):
        self.crawler = FacebookPageAttrs(self.driver)
        self.crawler.do_login(EMAIL, PASSWORD)

    def test_group_page_link_text(self):
        self.crawler = FacebookPageAttrs(self.driver)
        title = self.crawler.get_group_page_title()
        assert TestData.PAGE_TITLE in title

    def test_get_article_link(self):
        self.crawler = FacebookPageAttrs(self.driver)
        link_list = self.crawler.get_article_link()
        assert TestData.ARTICLE_LINK in str(link_list)

    def test_click_expand_button(self):
        self.crawler = FacebookPageAttrs(self.driver)
        click_message = self.crawler.click_expand_button()
        assert TestData.CLICK == click_message

    # def test_get_article_title(self):
    #     self.crawler = FacebookPageAttrs(self.driver)
    #     title_exist = self.crawler.get_article_title()
    #     assert title_exist
    #
    # def test_get_article_message_name_boxes(self):
    #     self.crawler = FacebookPageAttrs(self.driver)
    #     name_exist = self.crawler.get_article_message_name_boxes()
    #     assert name_exist
    #
    # def test_get_article_message_content_boxes(self):
    #     self.crawler = FacebookPageAttrs(self.driver)
    #     content_exist = self.crawler.get_article_message_content_boxes()
    #     assert content_exist

    def test_mongodb_data(self, log):
        self.crawler = FacebookPageAttrs(self)
        data = self.crawler.get_data()
        assert len(data['article_id']) == 15
        assert 'posts' in data['article_link']
        assert data['article_title'] is not int
        assert type(data['article_message']) == list
