from urllib.request import urlretrieve
import os
import csv

import errno

CSV_IMAGE_LIST_LINK = "../output/image_list.csv"
BASE_URL = "https://www.examveda.com"
IMAGE_URL_ROW = 'urls'

total_image = 0

with open(CSV_IMAGE_LIST_LINK) as csvfile:
    reader = csv.reader(csvfile)

    total_image = sum(1 for row in reader)

total_image -= 1 # remove header

with open (CSV_IMAGE_LIST_LINK) as csv_file:
    img_count = 1
    reader = csv.DictReader(csv_file)

    image_count = 1
    for row in reader:
        print(str(image_count) + "/" + str(total_image))
        print(row['urls'])
        image_count +=1

        filename = '.' + row[IMAGE_URL_ROW] 
        url = BASE_URL + row[IMAGE_URL_ROW]
        img_count = img_count + 1


     #   if os.path.exists(row[IMAGE_URL_ROW]):
     #       print("file exist " + row[IMAGE_URL_ROW])
     #       continue
     #   else:
        

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        print("get image :" , url)
        urlretrieve(url, filename)
