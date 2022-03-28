import os
import sys
import re
import time
import pymongo

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cur_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(cur_path)[0]
sys.path.append(os.path.split(rootPath)[0])
#  因為所在路徑是python的搜索路徑，如果涉及到import引用就會報類似ImportError: No module named xxx這樣的錯誤.
#  設定路徑後即可在cmd執行.

if True:  # noqa: E402
    from facebook_crawlers.src.crawler.settings import EMAIL, PASSWORD


class CrawlerFacebook:
    def __init__(self):
        self.driver = Service(r'C:\Users\han\Desktop\facebook-crawlers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values.notifications': 2,
            'excludeSwitches': ['enable-logging'],
            # settings something about can ignore error messages in command line.
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(service=self.driver, options=options)
        self.driver.maximize_window()
        time.sleep(2)
        self.account = EMAIL
        self.password = PASSWORD
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['GamesofaCareers']
        self.collections = db['ArticleList']

    def login(self):
        self.driver.get('https://www.facebook.com/')
        self.driver.find_element(By.ID, 'email').send_keys(self.account)
        self.driver.find_element(By.ID, 'pass').send_keys(self.password)
        self.driver.find_element(By.NAME, 'login').click()  # Login facebook.
        time.sleep(2)

    def get_link(self, limit):
        self.driver.get('https://www.facebook.com/GamesofaCareers')
        time.sleep(2)
        for _ in range(int(limit) - 1):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            # Scroll the page to the bottom to load the article.
            time.sleep(3)

        link_list = []
        post_links = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, '//div[@class="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"]'
                           '//a[@class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9'
                           ' nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9'
                           ' a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"]')))

        for post_link in post_links:
            ActionChains(self.driver).move_to_element(post_link).perform()
            # Mouse move to link location, Hover over to show links.
            link_list.append(post_link.get_attribute('href').split('?', 1)[0])
            time.sleep(2)

        return link_list

    def expand(self, url):
        self.driver.get(url)
        time.sleep(2)
        self.driver.refresh()
        time.sleep(4)
        count = 1
        while count != 0:
            count = 0
            for more_expand in self.driver.find_elements(
                    By.XPATH, '//div[@role="button"]'
                              '//span[@class="j83agx80 fv0vnmcu hpfvmrgz"]'
                              '//span[@dir="auto"]'):
                if bool(re.search('先前的留言|先前的回答|之前的答案|則留言', more_expand.text)) is True:
                    try:
                        more_expand.click()
                        print('More expand...')
                        time.sleep(2)
                    except NoSuchElementException as nse:
                        print('caught', nse)
                    time.sleep(2)
                    count += 1

    def comment(self, url):
        data = []
        article_id = url.split('posts/')[1].replace('/', '')

        try:
            title = self.driver.find_element(
                By.XPATH, '//div[@class="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"]'
                          '//div[@dir="auto"]').text.replace('\n', '')
        except (AttributeError, ValueError, KeyError):
            title = 'Sticker or Video'

        messages = []
        name_boxes = self.driver.find_elements(
            By.XPATH, '//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]'
                      '//a[@role="link"]//span[@class="pq6dq46d"]//span[@dir="auto"]')
        content_boxes = self.driver.find_elements(
            By.XPATH, '//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]'
                      '//div[@class="ecm0bbzt e5nlhep0 a8c37x1j"]'
                      '//div[@class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql"]')

        names = [name_box.text.replace('\n', '') for name_box in name_boxes]
        if len(names) != 0:
            names = names
        else:
            names = 'Anonymous user'

        contents = [content_box.text.replace('\n', '') for content_box in content_boxes]
        if len(contents) != 0:
            contents = contents
        else:
            contents = 'Sticker or Video'

        for name, content in zip(names, contents):
            messages.append(name + ':' + content)

        data.append({
            'article_id': article_id,
            'article_link': url,
            'article_title': title,
            'article_message': messages
        })

        print(f'Article {article_id} crawling successfully.')

        for post in data:
            self.collections.insert_one(post)

        return data

    def reset_mongo(self):
        return self.collections.delete_many({})


if __name__ == '__main__':
    run = CrawlerFacebook()
    run.reset_mongo()
    run.login()
    Links = run.get_link(1)
    print(f'Search {len(Links)} article, Start crawling.')
    for link in Links:
        print('Catch with:' + link)
        try:
            run.expand(link)
            run.comment(link)
        except (AttributeError, ValueError, KeyError):
            print(link, 'Catch failed.')
