import json
import random
import string
import re
import pkgutil
import scrapy

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs

class QuestionSpider(scrapy.Spider):
    name = "questions"
    allowed_domains = ["examveda.com"]

    main_id = 0
    topic_id =  0
    subject_id = 0
    topic_name = ""

    start_urls = []

    def __init__(self, topic='<NA>', **kwargs):
        '''
        jsondata = pkgutil.get_data("project", "resources/topic.json")

        print(type(jsondata))
        print("<DATA>")
        print(jsondata)

        return

        jdata = json.loads(jsondata)
        '''
        jdata = json.loads(open ('data_grab/resources/topic.json').read())

        topic_name = ""
        set_url = ""
        
        for c in jdata:
            if topic == c["topic_name"]:
                topic_name = topic
                self.main_id = c["main_id"]
                self.topic_id =  c["topic_id"]
                self.subject_id = c["subject_id"]
                set_url = c["topic_url"]
                break
                
        if topic_name == "":
            print ("Not Found " + topic )
        else:
            print ("Found " + topic )
            self.topic_name = topic_name
            self.start_urls = [set_url]
            super().__init__(**kwargs)
        
    def parse(self, response):
        url =  response.request.url
        parsed = urlparse(url)
        curr_section = -1

        has_section = len(response.css('.more-section a::attr(href)').extract()) + 1
        
        try:
            val = parse_qs(parsed.query)['page'][0]
            curr_page = int(val)
        except:
            curr_page = 1

        if (has_section>1):
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
                ques =  re.sub(r" class=\"question-main\"", "", ques)
                ques_no = ques_set.css('.question-number::text').extract_first()

                # Answer Manager
                ans = ques_set.css('input+ label').extract()
                ans_json = '['

                total_answers = len(ans)

                i_ans = 1

                for a in ans:
                    a = re.sub(r"</label>", "", a)
                    a = re.sub(r"<label.*?>", "", a)

                    ans[i_ans-1] = a

                    ans_json += '{\"option_value\": \"'
                    ans_json += a
                    ans_json += '\", \"optionl2_value\": \"\", \"has_file\": 0, \"file_name\": \"\"}'

                    if i_ans < total_answers:
                        ans_json += ","

                    i_ans += 1
    
                ans_json += ']'
            
                corr_ans_index = ques_set.css('.question-options input::attr(value)').extract()
                corr_ans = []
            
                for index in corr_ans_index:
                    i = int(index) - 1 
                    corr_ans.append(ans[i])

                ###########################

                # Meta and Slug  Manager
                meta_format = '{{topic_id:{topic_id}|topic:{topic}|section:{section}|page:{page}|question:{question}}}'

                meta = meta_format.format(
                    topic = self.topic_name,
                    topic_id = self.topic_id,
                    section = curr_section if curr_section > 0 else '-',
                    page = curr_page,
                    question= ques_no
                )

                slug = str(self.subject_id)+ id_generator() + str(self.topic_id)

                explanation = ques_set.css('.page-title~ div+ div').extract_first()
                explanation = explanation.replace('<span class=\"color\">Solution: </span>',"")
                explanation = explanation.replace("<div>","")
                explanation = explanation.replace("</div>","")
                explanation = explanation.strip()

                ###########################

                item = {
                    'meta': meta,
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
                    'explanation_file': "NULL",
                    'status': 1,
                    'created_at': "",
                    'updated_at': "",
                    'question_l2': ques,
                    'explanation_l2': explanation,
                    'correct_answers_value': corr_ans
                }
                
                '''
                item = {
                    'meta': meta,
                }
                '''
             
                yield item

        # follow pagination
        has_next_page = response.css('.icon-angle-right').extract_first()
        next_page = None
        
        if has_next_page is not None:
            if has_section>1:
                next_page = parsed.scheme + "://" + parsed.netloc + parsed.path + "?section=" + str(curr_section) + "&page=" + str(curr_page + 1)
            else:
                next_page = parsed.scheme + "://" + parsed.netloc + parsed.path + "?page=" + str(curr_page + 1)    
        elif (has_next_page is None and has_section and curr_section < has_section):
            curr_section = curr_section + 1
            next_page = parsed.scheme + "://" + parsed.netloc + parsed.path + "?section=" + str(curr_section) + "&page=1"
            
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

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