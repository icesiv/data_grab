import csv
import re
from os import listdir
from os.path import isfile, join

CSV_DATA_FOLDER = "output"
CSV_IMAGE_LIST_LINK = "image_grab/_list.csv"

image_list = []

def extract_image(text_with_link):
    jpgs = re.findall(r"\/public\/.*?JPG", text_with_link, re.MULTILINE)
    pngs = re.findall(r"\/public\/.*?PNG", text_with_link, re.MULTILINE)
    images = jpgs + pngs
    return(images)

def extract_from_file(file_link):
    with open(file_link) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        want_cl = ["question", "explanation"]

        for row in csv_reader:
            for val in want_cl:
                img_list = extract_image(row[val])

                if len(img_list) > 0:
                    for i in img_list:
                        image_list.append(i)

def export_image_list():
    with open(CSV_IMAGE_LIST_LINK, mode='w') as imageList_file:
        csv_writer = csv.writer(
            imageList_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(['urls'])

        for target_list in image_list:
            csv_writer.writerow([target_list])


onlyfiles = [f for f in listdir(CSV_DATA_FOLDER) if isfile(join(CSV_DATA_FOLDER, f))]
for target_file in onlyfiles:
    extract_from_file(CSV_DATA_FOLDER + "/" + target_file)

print("Image found : " + str(len(image_list)))
export_image_list()