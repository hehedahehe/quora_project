# -*- coding: utf-8 -*-

# Scrapy settings for quoraproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'quoraproject'

SPIDER_MODULES = ['quoraproject.spiders']
NEWSPIDER_MODULE = 'quoraproject.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 5

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'quoraproject.middlewares.QuoraprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'quoraproject.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'quoraproject.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

URLS =  [
    {"science": ("https://www.quora.com/topic/Science", \
                "https://tch610986.tch.quora.com/up/chan33-8888/updates?min_seq={min_seq}&channel=main-w-dep3302-4288939216925556691&hash=12865231918938351100"),},

    { "psychology": ("https://www.quora.com/topic/Psychology", \
                "https://tch273265.tch.quora.com/up/chan32-8888/updates?min_seq=0&channel=main-w-dep3702-365054163074802271&hash=15746322881662153920&timeout=2000"),},

    { "business": ("https://www.quora.com/topic/Business", \
                "https://tch730677.tch.quora.com/up/chan31-8888/updates?min_seq=0&channel=main-w-dep3704-546470324318062481&hash=7501771319431199530&timeout=2000"),},

    { "economics": ("https://www.quora.com/topic/Economics", \
                "https://tch432261.tch.quora.com/up/chan32-8888/updates?min_seq=0&channel=main-w-dep3204-2954796011848666925&hash=13214664269129467903&timeout=2000&callback=jsonp159cf3688aa2279f5f656f248"),},
    { "education": ("https://www.quora.com/topic/Education", \
                "https://tch981056.tch.quora.com/up/chan33-8888/updates?min_seq=0&channel=main-w-dep3604-576042793758136847&hash=10908539047893352143&timeout=2000"),},
    { "health": ("https://www.quora.com/topic/Health", \
                "https://tch399033.tch.quora.com/up/chan33-8888/updates?min_seq=0&channel=main-w-dep3202-1275439469913957844&hash=1921290174208687769&timeout=2000&callback=jsonp159cf374d8747e6b04638fed"),},
    { "software-engineering":("https://www.quora.com/topic/Software-Engineering",\
                "https://tch401091.tch.quora.com/up/chan31-8888/updates?min_seq=0&channel=main-w-dep3305-4351998901659315965&hash=15512808931192119355&timeout=2000&callback=jsonp159cf381f3ef2dac7b22c12d"),},
    { "life-and-living": ("https://www.quora.com/topic/Life-and-Living-2", \
                "https://tch275285.tch.quora.com/up/chan31-8888/updates?min_seq=0&channel=main-w-dep3304-410412573991406094&hash=17619718658876224271&timeout=2000&callback=jsonp159cf392dcf6a6f1da7df6ea"),},
    ]

INDEX=0

headers = {
    "Host": "www.quora.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #"Referer": 'https://www.quora.com/topic',
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": 'zh-CN,zh;q=0.8',
}

USERS_MAX = 10000
QUESTIONS_MAX = 10000
MAX_DEP = 2 # 问题的抓取深度