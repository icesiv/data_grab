from urllib.request import urlretrieve
import os.path
import csv

CSV_IMAGE_LIST_LINK = "output/image_list.csv"
BASE_URL = "https://www.examveda.com"
IMAGE_URL_ROW = 0

with open (CSV_IMAGE_LIST_LINK) as images:
    images = csv.reader(images)
    img_count = 1
    total_image = str(len(images))
    
    for i, row in enumerate(images):
        file_path = BASE_URL + row[IMAGE_URL_ROW]
        print(str(img_count) + "/" + total_image)
        img_count = img_count + 1
  
        #if img_count>10:
        #    break

        if os.path.exists(file_path):
            continue
        else:
            urlretrieve("GET FILE NAME",file_path) 

    