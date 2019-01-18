import csv
import os
import re
import sys
from os import listdir
from os.path import isfile, join
from urllib.request import urlretrieve

import PIL
from PIL import Image

CSV_DATA_FOLDER = "output"
CSV_IMAGE_LIST_LINK = "image_grab/_list.csv"
COLUMNS_WITH_IMAGES = ["image_list"]

BASE_URL = "https://www.examveda.com"

def resize_image(image_file_path):
    img = Image.open(image_file_path)
    basewidth = int(img.size[0] + (img.size[0] * .1))
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save(image_file_path)

def download_image(image_obj):
    if not image_obj:
        return

    image_obj = image_obj.split(":")

    filename = "." + image_obj[1]
    url = BASE_URL + image_obj[0] 

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except:  # Guard against race condition
            raise

    try:
        if os.path.exists(filename):
            print("duplicate")
        else:
            fName, head = urlretrieve(url, filename)

            if (head["Content-Type"] == "text/html; charset=UTF-8"):
                print("Error-- Not Found: ", filename)
                os.remove(filename)
            else:
                resize_image(filename)
                return 1

    except:
        print("Error-- ", sys.exc_info()[0])

    return 0


def extract_image(s):
    if(not s):
        return 0

    s = s.split("|")
    
    i = 0
    for c in s:
        download_image(c)
        i+=1

    return i

def extract_from_file(file_link):
    image_count = 0

    print("Processing File:",file_link)

    with open(file_link) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            for val in COLUMNS_WITH_IMAGES:
                try:
                    count = extract_image(row[val])
                except:
                    print("Error <Missing Column> : " , val)
                    continue

                image_count += count 

    print("Total Image found", image_count)

# >> Start >>>>>>>>>>>>>>>>>>>>

onlyfiles = [f for f in listdir(CSV_DATA_FOLDER) if isfile(join(CSV_DATA_FOLDER, f))]

for target_file in onlyfiles:
    extract_from_file(CSV_DATA_FOLDER + "/" + target_file)
