# coding:utf-8
import scrapy
from scrapy.selector import Selector
from ..settings import  USER_AGENT, URLS, INDEX, headers
from ..items import Topic, Question
import json


class QuoraSpider(scrapy.Spider):
    name = "quoraSpider"
    allowed_domains = ["quora.com", ]

    def start_requests(self):
        '''
        -science: https://www.quora.com/ topic / Science
        -psychology: https: // www.quora.com / topic / Psychology
        -business: https: // www.quora.com / topic / Business
        -economics: https: // www.quora.com / topic / Economics
        -education: https: // www.quora.com / topic / Education
        -health: https: // www.quora.com / topic / Health
        -software
        engineering: https: // www.quora.com / topic / Software - Engineering
        -Life and Living: https: // www.quora.com / topic / Life - and -Living - 2
        :return:
        '''


        urls = URLS[INDEX]
        for topic_name in urls:
            topicpage_url = urls[topic_name][0]  # 得到topic页面的url
            detail_url = urls[topic_name][1]  # 得到list页面起始url
            topic = Topic()
            topic["name"] = topic_name
            #yield scrapy.Request(url=topicpage_url, meta={"topic": topic}, headers=headers,callback=self.topicInfo_parse)  # 发起topic页面请求
            yield scrapy.Request(url=topicpage_url, meta={"topic": topic},callback=self.topicInfo_parse)  # 发起topic页面请求
            questions = []
            topic["questions"] = questions  # 关联该topic的所有问题

            # 发起请求，获取所有问题
            meta = {"questions":questions, "detail_url":detail_url,"topic_name": topic["name"],"counter":0}
            yield scrapy.Request(url=detail_url.format(min_seq=0), meta=meta, headers=headers, callback=self.listPage_parse)
            #yield scrapy.Request(url=detail_url.format(min_seq=0), meta=meta, callback=self.listPage_parse)


    def topicInfo_parse(self, response):
        '''
        得到topic信息
        :param response:
        :return:
        '''

        print("[DEBUG]Enter topic page parse. {url}".format(url=response.url))
        if response:
            topic = response.meta["topic"]
            topic["follower_num"] = response.xpath("//a[contains(@class, 'TopicFollowersStatsRow ')]/strong/text()").extract_first("").strip()
            topic["questions_num"] = response.xpath("//a[contains(@class, 'TopicQuestionsStatsRow')]/string/text()").extract_first("").strip()
            topic["edits_num"] = response.xpath("//a[contains(@class, 'TopicEditsStatsRow')]/strong/text()").extract_first("").strip()
            topic["about_info"] = response.xpath("//div[@class='TopicPageAboutSection']//span[@class='rendered_qtext']/text()").extract_first("").strip()
            topic["related_topics_info"] = []
            related_topics_selc = response.xpath("//a[contains(@class, 'RelatedTopicsListItem')]")
            for each in related_topics_selc:
                topic_url = each.xpath("./@href").extract_first("").strip();
                topic_url = response.urljoin(topic_url);
                topic_name = each.xpath(".//span[@class='TopicName']/text()").extract_first("").strip()
                topic["related_topics_info"].append((topic_name,topic_url))
            print("[DEBUG] topic follower_num: " + topic["follower_num"])
            print("[DEBUG] topic questions_num: " + topic["questions_num"])
            print("[DEBUG] topic about_info: " + topic["about_info"])
            print("[DEBUG] topic edits_num: " + topic["edits_num"])
            print("[DEBUG] topic related_topics_info: ")
            for each in topic["related_topics_info"]:
                print(each[0] + " : " + each[1])

        else:
            print("Wrong!")


    def listPage_parse(self, response):
        '''
        得到问题的url
        :param response:
        :return:
        '''
        print("[DEBUG]Enter listpage_parse. {url}".format(url=response.url))
        json_response = json.loads(response.text)
        if json_response:
            from ..utils.text_process import processMessage
            print(json_response["messages"])
            if json_response["messages"]:
                raw_message = json_response["messages"][0]
                message = processMessage(raw_message)

                #print("[RAW MESSAGE]:" + raw_message)
                #print("[MESSAGE]:" + message)
                #print("[MESSAGE]:" + str(min_seq))
                urls = []
                question_urls = Selector(text=message).xpath("//a[@class='question_link']/@href").extract()
                print("[DEBUG]: URLs...")
                print(question_urls)

            min_seq = json_response["min_seq"]
            detail_url = response.meta["detail_url"]
            questions = response.meta["questions"]
            topic_name = response.meta["topic_name"]
            counter = response.meta["counter"] + 1
            meta = {"questions":questions, "detail_url":detail_url,"topic_name": topic_name, "counter":counter}
            if counter<10:
                yield scrapy.Request(url=detail_url.format(min_seq=int(min_seq)), headers=headers,meta=meta, callback=self.listPage_parse)

        else:
            print("Wrong!")





