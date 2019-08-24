import config
import scrapy
import random
import re

from utils import id_generator

class StudyPressPSpider(scrapy.Spider):
    name = "studypress_practice"
    allowed_domains = ["icabd.com"]

    main_id = 0
    topic_id = 0
    subject_id = 0
    topic_name = ""

    start_urls = []

    def __init__(self, data_obj, go_next_page=True, **kwargs):
    
        self.go_next_page = go_next_page
    
        topic_name = data_obj["topic_name"]
        set_url = data_obj["topic_url"]

        self.main_id = data_obj["main_id"]
        self.topic_id = data_obj["topic_id"]
        self.subject_id = data_obj["subject_id"]
  
        self.topic_name = topic_name
        self.start_urls = [set_url]
        super().__init__(**kwargs)


    def parse(self, response):
        edited_body = str(response.body, 'UTF-8')
        edited_body = edited_body.replace("<p class=\"qmeta\">", "")

        edited_body = edited_body.replace("<ul class=\"list-group\">", "<article class=\"question single-question question-type-normal\"><ul>")
        edited_body = edited_body.replace("</ul>", "</ul></article>")
        
        edited_body = edited_body.replace("<li class=\"list-group-item list-ques\">", 
        "</ul></article>\n\r   <article class=\"question single-question question-type-normal\"><ul><li class=\"list-group-item list-ques\">")
       
       # f= open("test.html","w+")
        # f.write(edited_body)
        # f.close() 
      
        response = response.replace(body=edited_body)
        url = response.request.url
        
        count = 1

        for ques_set in response.css('.question-type-normal'):
            
            # Question  
            ques = ques_set.css('.list-ques').extract_first()
          
            if not ques:
                continue

            q_label = ques_set.css('.label-info::Text').extract_first()
            
            ques_pack = clean_question(ques , q_label)
            ques_no = ques_pack[0]
            ques =  ques_pack[1]
     
            # Answers  
            ans_set_temp = ques_set.css('.list-option').extract()
            ans_set = clean_answer(ans_set_temp)
            
            total_answers = len(ans_set)
        
            corr_ans_temp = ques_set.css('.list-hidden input::attr(value)').extract()
            corr_ans_temp = proper_index(corr_ans_temp)

            if len(corr_ans_temp)< 1 :
                print(ques_no , " >> !ERROR! No correct answer found !ERROR!")
                continue
        

            corr_ans = []
            for v_c in corr_ans_temp:
                for i_a, v_a in enumerate(ans_set):
                    if(v_c == i_a + 1):
                        corr_ans.append( v_a )

            random.shuffle(ans_set)

            corr_ans_index = []
            for v_c in corr_ans:
                for i_a, v_a in enumerate(ans_set):
                    if(v_c == v_a):
                        corr_ans_index.append( i_a + 1 )



            # Answer JSON
            ans_json = '['

            for i, a in enumerate(ans_set):
                ans_json += '{\"option_value\": \"'
                ans_json += a
                ans_json += '\", \"optionl2_value\": \"\", \"has_file\": 0, \"file_name\": \"\"}'

                if i < total_answers - 1:
                    ans_json += ","

            ans_json += ']'

            # Slug  
            slug = str(self.subject_id) + id_generator() + str(self.topic_id)
           
            # Explanation  
            explanation = ques_set.css('.list-hint').extract_first()

            if explanation == None:
                explanation = config.EXPLANATION_NEW(slug)
            else:
                explanation = explanation.replace('<li class=\"list-group-item list-hint\">', "")
                explanation = explanation.replace("<strong>", "")
                explanation = explanation.replace("</strong>", "")
                explanation = explanation.replace("</li>", "")
                explanation = explanation.replace("Explanation:", "")
                explanation = explanation.strip()

            # Output Item
            item = {
                'q_no': ques_no,
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
                'correct_answers_value': corr_ans,
                'image_list': ""
            }

            count = count + 1
            yield item

        print("Total Q found : ", count - 1 )


def proper_index(arr):
    for i, s in enumerate(arr):
        s = s.upper()
        if s == 'A' or s == 1:
            arr[i] = 1
        elif s == 'B' or s == 2:
            arr[i] = 2
        elif s == 'C' or s == 3:
            arr[i] = 3
        elif s == 'D' or s == 4:
            arr[i] = 4
        elif s == 'E' or s == 5:
            arr[i] = 5
        elif s == 'F' or s == 6:
            arr[i] = 6

    return arr

def clean_answer(ans_set_temp):
    ans_set = []

    for ans in ans_set_temp:
        ans = ans.strip()
        
        if ans == "":
            continue
        else:
            ans = ans.split(')',1)[1].replace("</li>", "")
            ans_set.append(ans.strip()) 
            
    return ans_set

def clean_question(ques_temp, q_label):
    ques_temp = ques_temp.split('/span>',1)[1]
    ques_temp = ques_temp.split('<input',1)[0]

    ques_temp = ques_temp.split('.',1)

    for i, s in enumerate(ques_temp):
        ques_temp[i] = s.strip()

    if q_label != "" and q_label != None :
        ques_temp[1] = "<div class='label-info'><i>" + q_label.strip() + "</i></div><br/><div class='question'>" + ques_temp[1] + '</div>'
    else:
        ques_temp[1] = "<div class='question'>" + ques_temp[1] + '</div>'
        
    return ques_temp