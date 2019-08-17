import sys
import json

from data_grab.run_scraper import Scraper

if(len(sys.argv)<2):
    print('Please Give topic name. e.g. "ModelTest01"')
    sys.exit()

topic = sys.argv[1]
data_obj = False

j_data = json.loads(open('data_grab/resources/topic_studypress.json').read())

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

scraper.run_spiders(data_obj)
