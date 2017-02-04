#coding:utf-8
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class QuestionURLSpider(scrapy.Spider):
    '''
    根据搜索关键词来获取问题
    '''
    name = "questionurlSpider"
    allowed_domains = ["quora.com", ]

    def start_requests(self):
        with open("../utils/topwords.txt","r") as tf:
            allwords = tf.read();

        allwords = allwords.split(",")

        #allwords = ["complaint",]
        raw_search_url = "https://www.quora.com/search?q={word}"
        for each in allwords:
            meta = {"word":each}
            yield scrapy.Request(url=raw_search_url.format(word=each), meta=meta, callback=self.questionPageParse,encoding='utf-8')


    def questionPageParse(self, response):
        if response.status==200:
            with open("../datasets/searchpage-{word}.txt".format(word=response.meta["word"]), "w") as rf:
                rf.write(response.text)
            linkXpath = "//div[@class='pagedlist_item']//a[@class='question_link']/@href"
            urls = response.xpath(linkXpath).extract()
            for index,each in enumerate(urls):
                urls[index] = response.urljoin(each)
                print each
            with open("../datasets/urls-{word}.txt".format(word=response.meta["word"]), "w") as rf:
                rf.write("\n".join(urls))

            with open("../datasets/zsuc.txt", "a") as rf:
                rf.write(response.meta["word"]+",")
