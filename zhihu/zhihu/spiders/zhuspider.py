# coding:utf-8
import scrapy
from zhihu.settings import account,password
from scrapy.http import Request

class ZhiHuSpider(scrapy.Spider):
    name = "zhihu"
    start_urls = [
        "https://www.zhihu.com/#signin",
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
            formdata={'email':account,'password':password},
            callback=self.after_login,
            method="POST",
            url="https://www.zhihu.com/login/email"
        )
        
    def after_login(self, response):
        return scrapy.Request("https://www.zhihu.com",self.parse_index)
        
    def parse_index(self, response):
        for item in response.xpath('//a[@class="question_link"]/text()').extract():
            print item
        # print response.body