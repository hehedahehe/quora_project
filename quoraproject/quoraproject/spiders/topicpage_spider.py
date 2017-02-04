#coding:utf-8
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from ..settings import *

class topicPageSpider(scrapy.Spider):
    '''
    解析topic页面
    '''
    name="topicpageSpider"
    allow_domains = ["quora.com",]

    def start_requests(self):
        urls = [
            "https://www.quora.com/topic/Science",
            "https://www.quora.com/topic/Psychology",
            "https://www.quora.com/topic/Business",
            "https://www.quora.com/topic/Economics",
            "https://www.quora.com/topic/Education",
            "https://www.quora.com/topic/Health",
            "https://www.quora.com/topic/Software-Engineering",
            "https://www.quora.com/topic/Life-and-Living-2",
        ]

        with open("topics_visited.txt","r") as tv:
            self.topics_visited = tv.read().split(",")

        self.question_counter = 0
        self.user_counter = 0

        for each in urls:
            yield scrapy.Request(url=each, callback=self.topicPageParse)

    def topicPageParse(self, response):
        xpath_topic_name = "//div[@class='TopicPhotoName']//span[contains(@class,'TopicNameSpan')]/text()"
        topic_name = response.xpath(xpath_topic_name).extract_first("").strip()
        if topic_name not in self.topics_visited:
            with open("topics_visited.txt", "a") as tv:
                tv.write(topic_name+",")
            self.topics_visited.append(topic_name)

            # 如果数量不够
            if self.question_counter < QUESTIONS_MAX or self.user_counter < USERS_MAX:
                # 得到topic页的问题链接
                xpath_question = "//a[@class='question_link']/@href"
                questions = response.xpath(xpath_question).extract()
                for index, each in enumerate(questions):
                    questions[index] = response.urljoin(each)
                with open("../datasets/questions/questions_urls.txt", "a") as uf:
                    uf.write("\n".join(questions))
                self.question_counter += len(questions)

                # 得到topic页的用户链接
                xpath_topicpage_user = "//a[@class='user']/@href"
                users = response.xpath(xpath_topicpage_user).extract()
                for index, each in enumerate(users):
                    users[index] = response.urljoin(each)
                with open("../datasets/users_urls.txt", "a") as uf:
                    uf.write("\n".join(users))

                self.user_counter += len(users)

                # 得到相关topic的链接
                xpath_related_topic = "//a[contains(@class,'RelatedTopicsListItem')]/@href"
                related_topics = response.xpath(xpath_related_topic).extract()
                for each in related_topics:
                    yield scrapy.Request(url=response.urljoin(each),callback=self.topicPageParse)

                # 得到all questions页面链接
                xpath_topic_questions_all = "//a[contains(@class,'TopicQuestionsStatsRow')]/@href"
                topic_questions_all = response.xpath(xpath_topic_questions_all).extract_first("").strip()
                yield scrapy.Request(url=response.urljoin(topic_questions_all), callback=self.questionAllPageParse)

                # 得到topic followers 页面链接
                xpath_topic_followers = "//a[contains(@class,'TopicFollowersStatsRow')]/@href"
                topic_followers = response.xpath(xpath_topic_followers).extract_first("").strip()
                yield scrapy.Request(url=response.urljoin(topic_followers), callback=self.followersPageParse)


    def questionAllPageParse(self, response):
        '''
        解析all questions页面，获取questions的链接
        :param response:
        :return:
        '''
        xpath_question = "//a[@class='question_link']/@href"
        questions = response.xpath(xpath_question).extract()
        for index, each in enumerate(questions):
            questions[index] = response.urljoin(each)
        with open("../datasets/questions/questions_urls.txt", "a") as uf:
            uf.write("\n".join(questions))

        self.question_counter += len(questions)


    def followersPageParse(self, response):
        '''
        解析followers页面, 获取followers的链接
        :param response:
        :return:
        '''
        xpath_users = "//a[@class='user']/@href"
        users = response.xpath(xpath_users).extract()
        for index, each in enumerate(users):
            users[index] = response.urljoin(each)
        with open("../datasets/users/user_urls.txt", "a") as uf:
            uf.write("\n".join(users))

        self.user_counter += len(users)


