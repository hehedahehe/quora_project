# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoraprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Topic(scrapy.Item):
    type_topic="question"  # 分为 专栏"zhuanlan"或者问题"question"，默认为问题
    name = scrapy.Field()  # 主题的名称
    followers = scrapy.Field()  # User[]#所有关注的用户
    follower_num = scrapy.Field()  # 关注者的数量
    edits_num = scrapy.Field()  # int #编辑次数
    related_topics = scrapy.Field()  # Topic[] #相关的话题
    related_topics_info = scrapy.Field()  # [(topicname,url),()]  目前只存储主题名称和链接
    about_info = scrapy.Field()  # 关于该主题的信息
    questions = scrapy.Field()# []关于该主题的所有问题
    questions_num = scrapy.Field() # 该主题下的所有问题的数量
    url = scrapy.Field()  # 该主题的地址


class Question(scrapy.Item):
    title = scrapy.Field()  # string 该问题的题目
    tags = scrapy.Field()  # string[] 该问题的tags
    follow_num = scrapy.Field()  # int 该问题的关注数目
    share_num = scrapy.Field()  # int 该问题的分享数目
    answer_num = scrapy.Field()  # int 该问题的所有答案数目
    answer_num_real = scrapy.Field()  # int 实际抓取的答案数目
    answers = scrapy.Field()  # Answer[] 该问题的所有答案
    # topic = None# 该问题所属的topic
    url = scrapy.Field()  # 该问题的地址
    description = scrapy.Field()  # 问题的描述
    related_questions = scrapy.Field()  # 相关的问题 Question[]


class Answer(scrapy.Item):
    respondent_name = scrapy.Field()  # 回答者的姓名
    respondent_url = scrapy.Field()  # 回答者的网址
    content = scrapy.Field()  # 回答的内容
    views_num = scrapy.Field()  # 回答的浏览量
    rank_num = scrapy.Field()  # 该回答的的位置

class User(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()  # 用户姓名 string
    identity_credential = scrapy.Field()  # 身份认证 string
    profile = scrapy.Field()  # 简介 string

    about_info = scrapy.Field()  #[{key:value},]
    knows_about = scrapy.Field()  # [{topic_name:[answers_num, answers_link, topic_link]},]
    answers = scrapy.Field()  #[{question_name: [views_num, url,answer_by_user_link]}, ]


    answers_num = scrapy.Field()  # 回答数量 int
    questions_num = scrapy.Field()  # 提问数量 int
    posts_num = scrapy.Field()  # post数量 int
    activity_num = scrapy.Field()  # 活动数量 int
    followers_num = scrapy.Field()  # 关注者数量 int
    following_num = scrapy.Field()  # 关注数量 int
    edits_num = scrapy.Field()  # edit数量 int
