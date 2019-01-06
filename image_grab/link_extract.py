import csv
import re

def extract_image(text_with_link):
    jpgs = re.findall(r"\/images\/.*?JPG", text_with_link , re.MULTILINE)
    pngs = re.findall(r"\/images\/.*?PNG", text_with_link , re.MULTILINE)
    images = jpgs + pngs
    return(images)


with open('out/out.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    # 0     meta 
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



    with open('out/image_list.csv', mode='w') as imageList_file:
        csv_writer = csv.writer(imageList_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csv_writer.writerow(['meta','type','url'])

        for target_list in image_list:
            csv_writer.writerow([target_list['meta'], target_list['type'], target_list['url']])

    print(f'Processed {line_count} lines.')



