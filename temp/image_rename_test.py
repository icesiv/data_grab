import ntpath
import re

IMAGE_LINK_OLD = "/images/solution-image/"
IMAGE_LINK_NEW = "/public/uploads/set01/"

image_list = []

def extract_link_from_text(text , slug):

    jpgs = re.findall(r"\/images\/.*?JPG", text, re.MULTILINE)
    #pngs = re.findall(r"\/image\/.*?PNG", text, re.MULTILINE)

    img_count = 0

    for j in jpgs:
        img_count += 1
        curr_dir_name = ntpath.dirname(j)
        new_dir_name = curr_dir_name.replace(IMAGE_LINK_OLD,IMAGE_LINK_NEW)
        
        
        curr_file_name = ntpath.basename(j)
        new_file_name = "q-{0}-{1}.png".format(slug,img_count) 

        new_file = new_dir_name + "/" + new_file_name

        text = text.replace(j,new_file)

        print(j)

        image_list.append( (j , new_file))

    return text

given_text = "When the hands"
new_text =  extract_link_from_text(given_text , "slug")

