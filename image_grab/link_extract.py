import csv
import re

CSV_DATA_FILE_LINK = "output/out.csv"
CSV_IMAGE_LIST_LINK = "image_grab/_list.csv"


def extract_image(text_with_link):
    jpgs = re.findall(r"\/images\/.*?JPG", text_with_link, re.MULTILINE)
    pngs = re.findall(r"\/images\/.*?PNG", text_with_link, re.MULTILINE)
    images = jpgs + pngs
    return(images)


with open(CSV_DATA_FILE_LINK) as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # 6	    question
    # 17	explanation

    image_list = []

    want_cl = ["question", "explanation"]

    for row in csv_reader:
        for val in want_cl:
            img_list = extract_image(row[val])

            if len(img_list) > 0:
                for i in img_list:
                    image_list.append(i)


with open(CSV_IMAGE_LIST_LINK, mode='w') as imageList_file:
    csv_writer = csv.writer(
        imageList_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(['urls'])

    for target_list in image_list:
        csv_writer.writerow([target_list])

print("Image found : " + str(len(image_list)))
