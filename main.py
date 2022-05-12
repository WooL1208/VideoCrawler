from argparse import ArgumentParser
from crawler_action import CrawlerAction
class Main:
    def __init__(self, args):
        self.counter = 0
        self.crawler_action = CrawlerAction(args)

    def start(self):
        self.crawler_action.browser_open()
        self.crawler_action.load_fullpage()
        if args.video:
            self.crawler_action.download_videos()
        if args.script:
            self.crawler_action.download_script()
        self.crawler_action.browser_close()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--search", type=str,
                        help="key words",
                        default="")
    parser.add_argument("--engine", type=int,
                        help="1. pexel \n 2. coverr(not usable)",
                        default=1)
    parser.add_argument("--video", action="store_true",
                        help="是否下載影片",
                        default=False)
    parser.add_argument("--script", action="store_true",
                        help="是否下載敘述",
                        default=False)
    parser.add_argument("--headless", action="store_true",
                        help="是否開啟瀏覽器",
                        default=False)
    args = parser.parse_args()

    crawler = Main(args)
    crawler.start()