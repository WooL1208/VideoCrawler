from time import sleep
from tqdm import tqdm
from crawler_method import CrawlerMethod


class CrawlerAction:
    def __init__(self, args):
        match args.engine:
            case 1:
                self.url = 'https://www.pexels.com/zh-tw/search/videos/'
                self.xpath = '//div[@class="photo-item__info"]/a'
                self.script_xpath = '//article'
            case _:
                print("input error: engine is not supported")

        self.keywords = args.search
        self.engine = args.engine
        self.driver_path = './chromedriver.exe'
        self.download_path = f'./data/{self.keywords}/'
        self.crawler_method = CrawlerMethod()
        self.driver = self.crawler_method.set_chrome(headless=args.headless)

    def browser_open(self):
        '''
        開啟指定網頁
        '''
        self.driver.get(self.url + self.keywords)

    def browser_close(self):
        '''
        關閉瀏覽器
        '''
        self.driver.close()

    def load_fullpage(self):
        '''
        把網頁滑到底確保所有元素都被載入
        '''
        print('正在等待頁面載入', flush=True)
        get_height_last = 0
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);")
            sleep(3)
            get_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight;")
            if get_height == get_height_last:
                break
            else:
                get_height_last = get_height

    def download_videos(self):
        '''
        下載影片
        '''
        self.crawler_method.create_folder(self.keywords)
        elements = self.crawler_method.find_all_elements(xpath=self.xpath, driver=self.driver)
        for index, element in enumerate(tqdm(elements)):
            try:
                self.crawler_method.url_download(element.get_attribute(
                    'href'), filename=self.download_path + f'video{index}.mp4')
                sleep(0.5)
            except Exception as e:
                print(e)

    def download_script(self):
        '''
        下載敘述
        '''
        self.crawler_method.create_folder(self.keywords)
        elements = self.crawler_method.find_all_elements(xpath=self.script_xpath, driver=self.driver)
        for element in tqdm(elements):
            try:
                self.crawler_method.script_download(element.get_attribute(
                    'data-meta-title'), filepath=self.download_path, filename=self.keywords)
                sleep(0.5)
            except Exception as e:
                print(e)
