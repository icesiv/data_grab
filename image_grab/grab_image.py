from urllib.request import urlretrieve
import os
import csv

CSV_IMAGE_LIST_LINK = "image_grab/_list.csv"
BASE_URL = "https://www.examveda.com"
IMAGE_URL_ROW = 'urls'

total_image = 0

with open(CSV_IMAGE_LIST_LINK) as csvFile:
    reader = csv.reader(csvFile)
    total_image = sum(1 for row in reader)

total_image -= 1 # remove header

with open (CSV_IMAGE_LIST_LINK) as csvFile:
    reader = csv.DictReader(csvFile)

    image_count = 1
    for row in reader:
        filename = '.' + row[IMAGE_URL_ROW] 
        url = BASE_URL + row[IMAGE_URL_ROW]
        
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except: # Guard against race condition
                raise

        try:
            if os.path.exists(filename):
                print(str(image_count) + "/" + str(total_image) + " - duplicate")
                continue
            else:
                print(str(image_count) + "/" + str(total_image))
                fName, head = urlretrieve(url, filename)

                if (head["Content-Type"] == "text/html; charset=UTF-8"):
                    print("Error-- Not Found: ", image_count)
                    os.remove(filename)

        except:
            print("Error-- ", image_count)

        image_count +=1