#import pkgutil
import csv
import json
import ntpath
import random
import re
import string
from os import listdir
from os.path import isfile, join

import config
import scrapy

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs

#################################################################


class QuestionSpider(scrapy.Spider):
    name = "questions"
    allowed_domains = ["examveda.com"]

    main_id = 0
    topic_id = 0
    subject_id = 0
    topic_name = ""

    start_urls = []

    def __init__(self, topic='<NA>', go_next_page=True, **kwargs):
        j_data = json.loads(open('data_grab/resources/topic.json').read())

        topic_name = ""
        set_url = ""

        self.go_next_page = go_next_page

        for c in j_data:
            if topic == c["topic_name"]:
                topic_name = topic
                self.main_id = c["main_id"]
                self.topic_id = c["topic_id"]
                self.subject_id = c["subject_id"]
                set_url = c["topic_url"]
                break

        if topic_name == "":
            print("<<Error>> [ Topic Not Found ] - " + topic)
        else:
            print("Topic Found - Please Wait")
            print("Target Page -", set_url)
            self.topic_name = topic_name
            self.start_urls = [set_url]
            super().__init__(**kwargs)

    def parse(self, response):
        url = response.request.url
        parsed = urlparse(url)
        curr_section = -1

        has_section = len(response.css(
            '.more-section a::attr(href)').extract()) + 1

        try:
            val = parse_qs(parsed.query)['page'][0]
            curr_page = int(val)
        except:
            curr_page = 1

        if (has_section > 1):
            try:
                val = parse_qs(parsed.query)['section'][0]
                curr_section = int(val)
            except:
                curr_section = 1

        for ques_set in response.css('.question-type-normal'):
            ques = ques_set.css('.question-main').extract_first()

            if not ques:
                continue
            else:
                ques = re.sub(r" class=\"question-main\"", "", ques)

                # Answer Manager
                ans = ques_set.css('input+ label').extract()

                # cleanup
                for i, a in enumerate(ans):
                    a = re.sub(r"</label>", "", a)
                    a = re.sub(r"<label.*?>", "", a)
                    ans[i] = a

                # correct answer
                corr_ans_index = ques_set.css(
                    '.question-options input::attr(value)').extract()
                corr_ans = []

                for index in corr_ans_index:
                    i = int(index) - 1
                    corr_ans.append(ans[i])

                # shuffle ans
                random.shuffle(ans)

                for i_c, v_c in enumerate(corr_ans):
                    for i_a, v_a in enumerate(ans):
                        if(v_c == v_a):
                            corr_ans_index[i_c] = i_a + 1

                total_answers = len(ans)
                ans_json = '['

                for i, a in enumerate(ans):
                    ans_json += '{\"option_value\": \"'
                    ans_json += a
                    ans_json += '\", \"optionl2_value\": \"\", \"has_file\": 0, \"file_name\": \"\"}'

                    if i < total_answers - 1:
                        ans_json += ","

                ans_json += ']'

                # Meta
                ques_no = ques_set.css(
                    '.question-number::text').extract_first().replace(". ", "")
                meta_format = '{{t_id:{topic_id}|t:{topic}|{section}p:{page}|q:{question}}}'

                if curr_section > 0:
                    s = "s:" + str(curr_section) + "|"
                else:
                    s = ""

                meta = meta_format.format(
                    topic=self.topic_name,
                    topic_id=self.topic_id,
                    page=curr_page,
                    section=s,
                    question=ques_no
                )

                # Slug  Manager
                slug = str(self.subject_id) + \
                    id_generator() + str(self.topic_id)

                # explanation Cleanup
                explanation = ques_set.css(
                    '.page-title~ div+ div').extract_first()

                if config.EXPLANATION_NOT_FOUND_TEXT in explanation:
                    explanation = config.EXPLANATION_NEW(slug)
                else:
                    explanation = explanation.replace(
                        '<span class=\"color\">Solution: </span>', "")
                    explanation = explanation.replace("<div>", "")
                    explanation = explanation.replace("</div>", "")
                    explanation = explanation.strip()

                # Replace Image Path

                image_list = ""

                from_explanation = extract_link_from_text(explanation , "exp-" + slug)
                
                if len(from_explanation[1]) > 0:
                    explanation = from_explanation[0]
                    image_list = from_explanation[1]

                from_ques = extract_link_from_text(ques , "ques-" + slug)
                
                if len(from_ques[1]) > 0:
                    ques = from_ques[0]
                    image_list += from_ques[1]
                
                ###########################

                item = {
                    'id': '',
                    'subject_id': self.subject_id,
                    'topics_id': self.topic_id,
                    'question_tags': self.topic_name,
                    'slug': slug,
                    'question_type': 'radio',
                    'question': ques,
                    'question_file': "",
                    'question_file_is_url': "0",
                    'total_answers': total_answers,
                    'answers': ans_json,
                    'total_correct_answers': len(corr_ans_index),
                    'correct_answers': corr_ans_index,
                    'marks': 5,
                    'time_to_spend': 60,
                    'difficulty_level': "easy",
                    'hint': "",
                    'explanation': explanation,
                    'explanation_file': "",
                    'status': 1,
                    'created_at': "",
                    'updated_at': "",
                    'question_l2': ques,
                    'explanation_l2': explanation,
                    'meta': meta,
                    'correct_answers_value': corr_ans,
                    'image_list': image_list
                }
                print("Q#", ques_no + "\t" + meta)

                yield item

        if not self.go_next_page:
            return

        # follow pagination
        has_next_page = response.css('.icon-angle-right').extract_first()
        next_page = None

        if has_next_page is not None:
            if has_section > 1:
                next_page = parsed.scheme + "://" + parsed.netloc + parsed.path + \
                    "?section=" + str(curr_section) + \
                    "&page=" + str(curr_page + 1)
            else:
                next_page = parsed.scheme + "://" + parsed.netloc + \
                    parsed.path + "?page=" + str(curr_page + 1)
        elif (has_next_page is None and has_section and curr_section < has_section):
            curr_section = curr_section + 1
            next_page = parsed.scheme + "://" + parsed.netloc + \
                parsed.path + "?section=" + str(curr_section) + "&page=1"

        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

###################################################################################################################################################

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


def extract_link_from_text(text_with_image, new_name):
    image_string = ""
    images = re.findall(r"\/images\/.*?JPG", text_with_image, re.MULTILINE)

    img_count = 0

    for j in images:
        img_count += 1
        new_dir_name = ntpath.dirname(j).replace(
            config.IMAGE_LINK_OLD, config.IMAGE_LINK_NEW)
        new_file_name = "{0}-{1}.png".format(new_name, img_count)
        new_file = new_dir_name + "/" + new_file_name

        text_with_image = text_with_image.replace(j, new_file)
        image_string = image_string + j + ":" + new_file + "|"

    return (text_with_image, image_string)
