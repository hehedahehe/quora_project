import scrapy

class LoginSpider(scrapy.Spider):
    name = 'loginSpider'
    start_urls = ['https://www.quora.com/webnode2/server_call_POST']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': '1246531124@qq.com', 'password': 'zzdxli'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        print("[DEBUG]: Enter after_login.")
        print(response.text)
