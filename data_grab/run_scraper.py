from data_grab.spiders.spider_examvida import ExamvidaSpider
from data_grab.spiders.spider_studypress import StudyPressSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        

    def run_spiders(self, data_obj, next_page=True):
        filename = 'output/' + data_obj["topic_name"] + '.csv'

        if data_obj["type"] == "practice":
            self.spiders = StudyPressSpider
        elif data_obj["type"] == "modeltest":
            self.spiders = StudyPressSpider 
        else:
            self.spiders = ExamvidaSpider

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

        self.process.crawl(self.spiders, data_obj, go_next_page=next_page)
        self.process.start()  # the script will block here until the crawling is finished