import sys
import json

from data_grab.run_scraper import Scraper

if(len(sys.argv)<2):
    print('Please Give topic name. e.g. "Clock"')
    sys.exit()

topic = sys.argv[1]
data_obj = False

j_data = json.loads(open('data_grab/resources/topic_examvida.json').read())

for c in j_data:
    if topic == c["topic_name"]:
        topic_name = topic
        data_obj = c
        break

if not data_obj:
    print("<<Error>> [ Topic Not Found ] - " + topic)
    sys.exit()

print("Topic Found - Please Wait")

scraper = Scraper()

if(len(sys.argv)>2):
    if(sys.argv[2]=="-y"):
        scraper.run_spiders(data_obj , False)
    else:
        scraper.run_spiders(data_obj)
else:
    scraper.run_spiders(data_obj)