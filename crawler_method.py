import os
import requests

from fake_useragent import UserAgent
from selenium import webdriver

class CrawlerMethod:
    def __init__(self):
        pass

    def create_folder(self, keywords):
        '''
        新增下載目標資料夾
        '''
        download_path = './data/'
        os.makedirs(download_path, exist_ok=True)
        download_path += keywords + '/'
        os.makedirs(download_path, exist_ok=True)

    def url_download(self, url, filename=None):
        '''
        使用requests來下載影片
        才不會被彈窗影響
        '''
        download_response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(download_response.content)

    def set_chrome(self, headless=False):
        '''
        設定瀏覽器：
        1. 偽裝user_agent
        2. 取消登入帳號
        3. 隱藏偽裝chromedriver
        4. 設定是否顯示瀏覽器畫面
        '''
        user_agent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent=%s' % user_agent.random)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {"profile.default_content_setting_value": {'notifications': 2}}
        options.add_experimental_option("prefs", prefs)
        if headless:
            options.add_argument('headless')
        else:
            options.add_argument('--start-maximized')
        browser = webdriver.Chrome(
            options=options, executable_path='./chromedriver')
        return browser
