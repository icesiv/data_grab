import random
import ntpath

import string
import re

##
# Random Generator
# --------------------------
# id_generator()
# >>> 'G5G74W'
#
# id_generator(3, "6793YUIO")
# >>>'Y3U'
##


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# #
# Extract Images From Text
# Changes Name in main


def extract_link_from_text(text_with_image, web_safe_topic, new_name):
    image_string = ""
    images = re.findall(r"\/images\/.*?JPG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?jpg", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?PNG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?png", text_with_image, re.MULTILINE)

    img_count = 0

    web_safe_topic = web_safe_topic + "/"

    for j in images:
        img_count += 1

        new_dir_name = ntpath.dirname(j) + "/"
        new_dir_name = new_dir_name.replace("solution-image/", "")
        new_dir_name = new_dir_name.replace(web_safe_topic, "")
        new_dir_name = new_dir_name.replace(config.IMAGE_LINK_OLD, config.IMAGE_LINK_NEW)
    
        new_file_name = "{0}-{1}.png".format(web_safe_topic + new_name, img_count)
        new_file_path = new_dir_name + new_file_name
    
        text_with_image = text_with_image.replace(j, new_file_path)
        image_string = image_string + j + ":" + new_file_path + "|"

    return (text_with_image, image_string)