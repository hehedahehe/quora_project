# -*- coding: utf-8 -*-

import scrapy
import json
from ..settings import headers
from ..items import User
class UserSpider(scrapy.Spider):
    name = "userSpider"
    allow_domains = ["quora.com",]

    def start_requests(self):
        urls = self.get_urls()
        #urls = ["https://www.quora.com/profile/Robert-Frost-1",
        #        "https://www.quora.com/profile/Richard-Muller-3",
        #        "https://www.quora.com/profile/Ian-York",
        #       "https://www.quora.com/profile/Joshua-Engel",
        #   ]

        for each in urls:
            yield scrapy.Request(url=each, headers=headers,callback=self.user_page_parse)


    def user_page_parse(self, response):
        print("[Enter user_page_parse]: {url}".format(url=response.url))

        user = User()
        self.init_user(user)

        xpath_name = "//span[@class='user']/text()"
        xpath_identity_credential = "//span[contains(@class,'IdentityCredential')]/text()"
        xpath_profile = "//span[contains(@class,'SimpleToggle')]/text()"
        xpath_about_info = "//div[@class='AboutSection']//div[contains(@class,'AboutListItem')]"
        xpath_knows_about = "//li[contains(@class,'ProfileExperienceItem')]//div[contains(@class,'TopicPreviewBioAnswers')]"
        xpath_answers = "//div[contains(@class,'AnswerListItem')]"
        xpath_answers_num = "//li[contains(@class,'AnswersNavItem')]//span[@class='list_count']/text()"
        xpath_questions_num = "//li[contains(@class,'QuestionsNavItem')]//span[@class='list_count']/text()"
        xpath_posts_num = "//li[contains(@class,'PostsNavItem')]//span[@class='list_count']/text()"
        xpath_activity_num = "//li[contains(@class,'ActivityNavItem')]//span[@class='list_count']/text()"
        xpath_followers_num = "//li[contains(@class,'FollowersNavItem')]//span[@class='list_count']/text()"
        xpath_following_num = "//li[contains(@class,'FollowingNavItem')]//span[@class='list_count']/text()"
        xpath_edits_num = "//li[contains(@class,'EditableListItem')]//span[@class='list_count']/text()"

        user["url"] = response.url
        user["name"] = response.xpath(xpath_name).extract_first("").strip()
        user["identity_credential"] = response.xpath(xpath_identity_credential).extract_first("").strip()
        user["profile"] = response.xpath(xpath_profile).extract_first("").strip()
        user["answers_num"] = response.xpath(xpath_answers_num).extract_first("").strip()
        user["questions_num"] = response.xpath(xpath_questions_num).extract_first("").strip()
        user["posts_num"] = response.xpath(xpath_posts_num).extract_first("").strip()
        user["activity_num"] = response.xpath(xpath_activity_num).extract_first("").strip()
        user["followers_num"] = response.xpath(xpath_followers_num).extract_first("").strip()
        user["edits_num"] = response.xpath(xpath_edits_num).extract_first("").strip()
        user["following_num"] = response.xpath(xpath_following_num).extract_first("").strip()
        #user[""] = response.xpath()

        user["about_info"] = []
        sels_about_info = response.xpath(xpath_about_info)
        for each_sel in sels_about_info:
            about_key = ''.join([each.strip() for each in each_sel.xpath(".//span[@class='main_text']//text()").extract() if each.strip()])
            about_detail = ''.join([each.strip() for each in each_sel.xpath(".//span[@class='detail_text']//text()").extract() if each.strip()])
            user["about_info"].append({about_key:about_detail})

        # [{topic_name:[answers_num, answers_link, topic_link]},]
        user["knows_about"] = []
        sels_knows_about = response.xpath(xpath_knows_about)
        for each_sel in sels_knows_about:
            topic_name = each_sel.xpath(".//span[contains(@class,'opicNameSpan')]").extract_first("").strip()
            topic_link = response.urljoin(each_sel.xpath(".//div[@class='topic_info']/a[contains(@class,'topic_name')]/@href").extract_first("").strip())
            answers_link = response.urljoin(each_sel.xpath(".//div[@class='topic_info']//a[@class='answer_link']/@href").extract_first("").strip())
            answers_num = each_sel.xpath(".//div[@class='topic_info']//a[@class='answer_link']/text()").extract_first("").strip()

            user["knows_about"].append({topic_name:[answers_num,answers_link,topic_link]})

        #[{question_name: [views_num, url,answer_by_user_link]}, ]
        user["answers"] = []
        sels_answers = response.xpath(xpath_answers)
        for each_sel in sels_answers:
            question_name = each_sel.xpath(".//a[@class='question_link']//span[@class='rendered_qtext']/text()").extract_first("").strip()
            views_num = each_sel.xpath(".//div[contains(@class,'answer_text')]//span[@class='meta_num']/text()").extract_first('').strip()
            answer_by_user_link = each_sel.xpath(".//a[@class='more_link']/@href").extract_first("").strip()
            question_url = response.urljoin(each_sel.xpath(".//a[@class='question_link']/@href").extract_first("").strip())
            if not views_num:
                views_num = -1 # -1 代表暂时无法获取views数量
            user["answers"].append({question_name:[question_url,answer_by_user_link,views_num]})

        self.dump_user(user)


    def dump_user(self, user):
        json_data = json.dumps(user, cls=UserEncoder)
        with open("../datasets/users/{name}.json".format(name=user["name"]), "w") as df:
            df.write(json_data)

    def get_urls(self):
        with open("../datasets/users/user_urls.txt","r") as uf:
            urls = uf.read().split("\n")
        return urls

    def init_user(self, user):
        user["name"] = ""
        user["identity_credential"] = ""
        user["profile"] = ""
        user["about_info"] = ""
        user["knows_about"] = []
        user["answers"] = []
        user["answers_num"] = 0
        user["questions_num"] = 0
        user["posts_num"] = 0
        user["activity_num"] = 0
        user["followers_num"] = 0
        user["following_num"] = 0
        user["edits_num"] = 0
        #user[""] =

class UserEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            knows_about = o["knows_about"]
            answers = o["answers"]
            return {o["name"]:{"name":o["name"],"identity_credential":o["identity_credential"],"profile":o["profile"],\
                               "about_info":o["about_info"],"knows_about":knows_about,"answers":answers,\
                               "answers_num":o["answers_num"],"questions_num":o["questions_num"],
                               "posts_num": o["posts_num"],"activity_num": o["activity_num"],"followers_num": o["followers_num"],\
                               "following_num": o["following_num"],"edits_num": o["edits_num"],"url":o["url"]}}
        else:
            return json.JSONEncoder.default(self, o)

