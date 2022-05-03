import os
import time
import requests
import wget
from argparse import ArgumentParser

from fake_useragent import UserAgent
from selenium import webdriver

class Main(object):
    def __init__(self, args):
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
        user_agent = UserAgent()
        headers = {
            '"Accept"="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"',
            '"Accept-Encoding"="gzip, deflate, br"',
            '"Accept-Language"="zh-TW,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5"',
            '"Host"={self.url}',
            '"Sec-Ch-Ua"="\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\""',
            '"Sec-Ch-Ua-Mobile"="?0"',
            '"Sec-Ch-Ua-Platform"="\"Windows\""',
            '"Sec-Fetch-Dest"="document"',
            '"Sec-Fetch-Mode"="navigate"',
            '"Sec-Fetch-Site"="none"',
            '"Sec-Fetch-User"="?1"',
            '"Upgrade-Insecure-Requests"="1"',
            '"User-Agent"={user_agent.random}'
        }

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--disable-blink-features=AutomationControlled")
        for argument in headers:
            options.add_argument(argument)

        if headless:
            options.add_argument('headless')
        else:
            options.add_argument('--start-maximized')

        if download_path is not None:
            os.makedirs(download_path, exist_ok=True)
            download_path += self.keywords + '/'
            os.makedirs(download_path, exist_ok=True)
            prefs = {"profile.default_content_setting_value": {'notifications': 2}, "profile.default_content_setting.popups": 0, "download.default_directory": download_path}
            options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(
            options=options, executable_path='./chromedriver')
        return browser

    def search(self):
        self.driver.get(self.url + self.keywords)

    def load_fullpage(self):
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
        self.search()
        # self.load_fullpage()
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
