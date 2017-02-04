# -*- coding: utf-8 -*-
import scrapy, json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..utils import tool
from ..items import  Question, Answer
from ..settings import  MAX_DEP, headers

class QuestionsSpider(scrapy.Spider):
    name = "questionsSpider"
    allow_domains = ["quora.com", ]

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        #for parent_question in self.parent_questions:
        #    print "[QuestionName]:" + parent_question["title"]
        #    self.dump_question_to_file(parent_question)
        pass

    def start_requests(self):
        #获取questions urls
        #self.parent_questions = []
        #meta = {"depth": 1, "parent_questions": self.parent_questions}
        all_question_urls = self.get_all_urls()
        #all_question_urls = ["https://www.quora.com/What-are-some-odd-or-generally-unknown-facts-about-outer-space", ]
        for each in all_question_urls:
            #parent_question = None
            #meta = {"depth": 1, "parent_question": parent_question}
            meta = {"depth": 1,}
            yield scrapy.Request(url=each, headers=headers,meta=meta, callback=self.question_page_parse)


    def question_page_parse(self, response):
        if response:
            depth = response.meta["depth"]
            #parent_question = response.meta["parent_question"]
            #print "[PARENT QUESTION]: " + str(parent_question)
            #self.parent_questions = response.meta["parent_questions"]
            if depth <= MAX_DEP:
                xpath_question_name = "//div[contains(@class,'question_text_edit')]//span[@class='rendered_qtext']/text()"
                xpath_tags = "//span[contains(@class,'TopicNameSpan')]/text()"
                xpath_question_desc = "//div[contains(@class,'question_details_text')]/span[@class='rendered_qtext']/text()"
                xpath_answers_number = "//div[@class='answer_count']/text()"

                question = Question()
                self.init_object(question)
                question["title"] = response.xpath(xpath_question_name).extract_first("").strip()
                question["description"] = response.xpath(xpath_question_desc).extract_first("").strip()
                question["tags"] = response.xpath(xpath_tags).extract()
                question["answer_num"] = response.xpath(xpath_answers_number).extract_first("").strip()
                question["url"] = response.url

                question["answers"] = []
                xpath_answers = "//div[@class='AnswerListDiv']//div[contains(@class,'AnswerPagedList')]//div[@class='Answer AnswerBase']"
                xpath_respondent_url = ".//span[contains(@class,'feed_item_answer_user')]//a[contains(@class,'user')]/@href"
                xpath_respondents_name = ".//span[@class='feed_item_answer_user']//a[contains(@class,'user')]/text()"
                xpath_answer_content = ".//div[contains(@id,'answer_content')]//span[contains(@class,'rendered_qtext')]//text()"
                xpath_answers_number = ".//span[@class='meta_num']/text()"
                selectors_answers = response.xpath(xpath_answers)
                question["answer_num_real"] = len(selectors_answers)
                for index, each in enumerate(selectors_answers):
                    ans = Answer()
                    self.init_object(ans)
                    ans["content"] = " ".join(each.xpath(xpath_answer_content).extract())
                    ans["views_num"] = each.xpath(xpath_answers_number).extract_first("").strip()
                    ans["respondent_name"] = each.xpath(xpath_respondents_name).extract_first("").strip()
                    ans["respondent_url"] = response.urljoin(each.xpath(xpath_respondent_url).extract_first("").strip())

                    ans["rank_num"] = index + 1
                    question["answers"].append(ans)
                # 若parent_question 为None, 即depth=1
                #if not parent_question:
                 #   parent_question = question
                    #self.parent_question["related_questions"] = []
                    #print "[Assign parent_questions]"
                 #   parent_question["related_questions"] = []
                 #   self.parent_questions.append(parent_question)
                 #   print "[Assign parent_questions]: length is {n}".format(n=len(self.parent_questions))
                #else:
                #    parent_question["related_questions"].append(question)


                xpath_related_questions_urls = "//ul[@class='list_contents']/li[@class='related_question']//a[@class='question_link']/@href"

                related_questions_urls = response.xpath(xpath_related_questions_urls).extract()
                question["related_questions"] = [response.urljoin(each) for each in related_questions_urls]
                self.dump_question_to_file(question)

                #meta = {"depth": depth + 1, "parent_question": parent_question}
                #for each in related_questions_urls:
                #    yield scrapy.Request(url=response.urljoin(each), headers=headers,meta=meta, callback=self.question_page_parse)

                meta = {"depth": depth + 1,}
                for each in related_questions_urls:
                    yield scrapy.Request(url=response.urljoin(each), headers=headers, meta=meta,
                                            callback=self.question_page_parse)
            else:
                pass
                #self.dump_question_to_file(parent_question)


    def get_all_urls(self):
        with open("../datasets/questions/questions_urls.txt","r") as question_file:
            all_question_urls = question_file.read().split("\n")
        print "[NUMBER]:{num}".format(num=len(all_question_urls))
        dir_path = "../datasets/"
        url_files = tool.get_files(dir_path, tool.file_condition)
        for each in url_files:
            with open(dir_path+each) as url_file:
                f_content = url_file.read()
                for each_url in f_content.split("\n"):
                    if each_url not in all_question_urls:
                        all_question_urls.append(each_url.strip())

        print "[NUMBER]:{num}".format(num=len(all_question_urls))

        return all_question_urls

    def dump_question_to_file(self, parent_question):
        json_data = json.dumps(parent_question, cls=MyJsonEncoder)
        with open("../datasets/questions/{name}.json".format(name=parent_question["title"]),"a") as df:
            df.write(json_data)




class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Answer):
            return {"respondent_name": o["respondent_name"], "respondent_url": o["respondent_url"],
                    "content": o["content"],
                    "views_num": o["views_num"], "rank_num": o["rank_num"]}
        elif isinstance(o, Question):
            return {o["title"]: {"title": o["title"], "tags": o["tags"], "answer_num": o["answer_num"],
                                    "answer_num_real": o["answer_num_real"], \
                                    "url": o["url"], "description": o["description"],
                                    "answers": json.loads(json.dumps(o["answers"],cls=MyJsonEncoder)),
                                    "related_questions": json.loads(json.dumps(o["related_questions"],cls=MyJsonEncoder))}}
        elif isinstance(o, list):
            if len(list)>0:
                if isinstance(o[0], Answer):
                    #如果是Answer列表
                    return [json.loads(json.dumps(each,cls=MyJsonEncoder)) for each in o]
                elif isinstance(o[0], Question):
                    #如果是Question
                    return [json.loads(json.dumps(each,cls=MyJsonEncoder)) for each in o]
        else:
            return json.JSONEncoder.default(self, o)

