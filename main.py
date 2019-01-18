import sys
from data_grab.run_scraper import Scraper


scraper = Scraper()

if(len(sys.argv)>2):
    if(sys.argv[2]=="-y"):
        scraper.run_spiders(sys.argv[1] , False)
    else:
        scraper.run_spiders(sys.argv[1])
else:
    scraper.run_spiders(sys.argv[1])
