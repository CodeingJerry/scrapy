# coding:utf-8
import scrapy
from scrapy.http import Request
from xiubai.items import XiubaiItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule

# class QiuBaiSpider(CrawlSpider):
    # name = "qiubai"
    # start_urls = [
        # "http://www.qiushibaike.com/",
    # ]
    # rules = [
        # Rule(LinkExtractor(allow="/article/*")),
        # Rule(LinkExtractor(allow="/users/*"),callback="parse_name"),
    # ]
    # # 请求的个人主页
    # def parse_name(self,response):
        # print response.xpath("//div[@class='user-header-cover']/h2/text()").extract()[0]


class QiuBaiSpider(scrapy.Spider):
    name = "qiubai"
    start_urls = [
        "http://www.qiushibaike.com/",
    ]
    
    def parse(self,response):
        extractor = LinkExtractor(allow="/article/*")
        links = extractor.extract_links(response)
        for link in links:
            item = XiubaiItem()
            req = Request(link.url, self.parse_detail_page)
            req.meta['item'] = item
            yield req
    
        #first method
        # for href in response.xpath('//span[@class="stats-comments"]/a/@href').extract():
            # detail_url = response.urljoin(href)
            # req = Request(detail_url, self.parse_detail_page)
            # item = XiubaiItem()
            # req.meta['item'] = item
            # yield req
            
    def parse_detail_page(self, response):
        item = response.meta['item']
        item['author'] = response.xpath('//div[@class="author clearfix"]/a[2]/h2/text()').extract()[0] if response.xpath('//div[@class="author clearfix"]').extract() else ''
        item['content'] = response.xpath('//div[@class="content"]/text()').extract()[0]
        comments = []
        for comment in response.xpath('//div[starts-with(@class, "comment-block clearfix floor")]'):
            comment_author = comment.xpath('./div[2]/a/text()').extract()[0]
            raw_content = comment.xpath('./div[2]/span/text()').extract()
            if len(raw_content) > 0:
                comment_content = raw_content[0]
            else:
                comment_content = ''
            comments.append({'comment_author':comment_author, 'comment_content':comment_content})
            item['comments'] = comments
        yield item
            
     