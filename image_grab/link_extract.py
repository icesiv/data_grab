import csv
import re

CSV_DATA_FILE_LINK = "output/out.csv"
CSV_IMAGE_LIST_LINK = "output/image_list.csv"

def extract_image(text_with_link):
    jpgs = re.findall(r"\/images\/.*?JPG", text_with_link , re.MULTILINE)
    pngs = re.findall(r"\/images\/.*?PNG", text_with_link , re.MULTILINE)
    images = jpgs + pngs
    return(images)

with open(CSV_DATA_FILE_LINK) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    # 6	    question
    # 17	explanation

    image_list = []

    want_cl = {
		"question" : 6,
		"explanation" : 17
	}
    
    for row in csv_reader:
        if line_count > 0:
            for key,val in want_cl.items():
                img_list = extract_image(row[val])

                if len(img_list)>0:
                        for i in img_list:
                            img_details = {
                                "meta" : row[0],
                                "type" : key,
                                "url" : i
                            }
                            
                            image_list.append(img_details)
            
        line_count += 1


    with open(CSV_IMAGE_LIST_LINK, mode='w') as imageList_file:
        csv_writer = csv.writer(imageList_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(['meta','type','url'])

        for target_list in image_list:
            csv_writer.writerow([target_list['meta'], target_list['type'], target_list['url']])

    print(f'Processed {line_count} lines.')



