from data_grab.spiders.question_spider import QuestionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spiders = QuestionSpider # The spider you want to crawl

    def run_spiders(self, topic):
        filename = 'output/' + topic + '.csv'

        self.process = CrawlerProcess({
            'FEED_URI': filename,
            'FEED_FORMAT': 'csv',
            'LOG_LEVEL': 'ERROR',
            'DOWNLOAD_DELAY': 3,
        })

        try:
            if os.path.exists(filename):
                print("Removing previous file - ", filename)
                os.remove(filename)
        except:
            print("Error On File Check")

        self.process.crawl(self.spiders, topic=topic)
        self.process.start()  # the script will block here until the crawling is finished