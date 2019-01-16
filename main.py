import sys
from data_grab.run_scraper import Scraper


scraper = Scraper()
scraper.run_spiders(sys.argv[1])
