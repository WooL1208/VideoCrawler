import os
import time
import requests
import wget
from argparse import ArgumentParser

from fake_useragent import UserAgent
from selenium import webdriver


class Main(object):
    '''
    probrom:
        1. 網頁會有彈出窗格
        2. 下載路徑無法變更
    to-do:
        1. 加入自動關閉彈出窗格
        2. 嘗試wget和requests方法下載影片
    '''

    def __init__(self, args):
        '''
        初始化
        設定各種變數
        '''
        match args.engine:
            case 1:
                self.url = 'https://www.pexels.com/zh-tw/search/videos/'
                self.xpath = '//div[@class="photo-item__info"]/a'
            case _:
                print("input error: engine is not supported")
        self.counter = 0
        self.driver_path = './chromedriver.exe'
        self.keywords = args.search
        self.engine = args.engine
        self.driver = self.new_chrome_browser(
            headless=args.headless, download_path='./data/')
        self.download = './data/'

    def new_chrome_browser(self, headless=True, download_path=None):
        '''
        設定瀏覽器
        '''
        user_agent = UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent=%s' % user_agent.random)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")

        if headless:
            options.add_argument('headless')
        else:
            options.add_argument('--start-maximized')

        '''
        更改預設下載路徑
        windows: 還沒測試
        mac: 目前無效
        '''
        if download_path is not None:
            os.makedirs(download_path, exist_ok=True)
            download_path += self.keywords + '/'
            os.makedirs(download_path, exist_ok=True)
            prefs = {"profile.default_content_setting_value": {'notifications': 2},
                     "profile.default_content_setting.popups": 0,
                     "download.default_directory": download_path}
            options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(
            options=options, executable_path='./chromedriver')
        return browser

    def search(self):
        '''
        開啟指定網頁
        '''
        self.driver.get(self.url + self.keywords)

    def load_fullpage(self):
        '''
        把網頁滑到底確保所有元素都被載入
        '''
        print('正在等待頁面載入', flush=True)
        get_height_last = 0
        while True:
            # 滑到頁底
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            get_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight;")
            if get_height == get_height_last:
                break
            else:
                get_height_last = get_height

    def download_videos(self):
        '''
        下載影片

        to-do:
        如果有X按鈕就按下去
        class name: js-modal-close-button rd__button rd__button--text-secondary rd__button--circle-icon--small
        '''
        elements = self.driver.find_elements_by_xpath(self.xpath)

        # 等待Response
        total = 0
        print('\r正在等待Response', flush=True)
        while total != len(elements):
            total = len(elements)
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            elements = self.driver.find_elements_by_xpath(self.xpath)

        for element in elements:
            try:
                element.click()
                print(element)
                time.sleep(0.5)
                self.counter += 1
            except Exception as e:
                pass
            print('\r%4d / %4d ( 已下載圖片數 / 已找到影片標籤數 )' %
                  (self.counter, total), flush=True)

    def start(self):
        '''
        開始執行
        '''
        self.search()
        self.load_fullpage()
        self.download_videos()
        return self.counter


if __name__ == '__main__':
    total = 0
    parser = ArgumentParser()
    parser.add_argument("--search", type=str,
                        help="key words",
                        default="")
    parser.add_argument("--engine", type=int,
                        help="1. pexel \n 2. coverr",
                        default=0)
    parser.add_argument("--headless", action="store_true",
                        help="是否開啟瀏覽器",
                        default=False)
    args = parser.parse_args()

    crawler = Main(args)
    total += crawler.start()
    print('\n總下載數：' + str(total))
    # crawler.driver.close()
