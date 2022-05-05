import time
from crawler_method import CrawlerMethod

class CrawlerAction:
    def __init__(self, args):
        self.counter = 0
        match args.engine:
            case 1:
                self.url = 'https://www.pexels.com/zh-tw/search/videos/'
                self.xpath = '//div[@class="photo-item__info"]/a'
            case _:
                print("input error: engine is not supported")

        self.driver_path = './chromedriver.exe'
        self.keywords = args.search
        self.engine = args.engine
        self.crawler_method = CrawlerMethod()
        self.driver = self.crawler_method.set_chrome(headless=args.headless)

    def browser_open(self):
        '''
        開啟指定網頁
        '''
        self.driver.get(self.url + self.keywords)

    def browser_close(self):
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
        '''
        download_path = f'./data/{self.keywords}/'
        self.crawler_method.create_folder(self.keywords)

        elements = self.driver.find_elements_by_xpath(self.xpath)
        total = 0
        print('\r正在等待Response', flush=True)
        while total != len(elements):
            total = len(elements)
            elements = self.driver.find_elements_by_xpath(self.xpath)
        for index, element in enumerate(elements):
            try:
                self.crawler_method.url_download(element.get_attribute('href'), filename=download_path + f'video{index}.mp4')
                # print(index, element.get_attribute('href'))
                time.sleep(0.5)
                self.counter += 1
            except Exception as e:
                print(e)

            print('\r%4d / %4d ( 已下載圖片數 / 已找到影片標籤數 )' %
                  (self.counter, total), flush=True)
