# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from autohome.items import AutohomeItem

class AutohomeCrawlSpider(CrawlSpider):
    name = 'autohome_crawl'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/price']
    rules = (
        Rule(LinkExtractor(allow=r'.+price/list-0-0-0-0-0-0-0-1-0-0-0-0-0-0-0-\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = AutohomeItem()
        print('_'*90)
        print(response.url+'\n')
        print('_'*90)
        auto_list = response.xpath('//div[@class="list-cont-bg"]')
        print('_'*90)
        for auto in auto_list:
            item["model_name"] = auto.xpath('.//a[@class="font-bold"]/text()').get()
            item["level"] = auto.xpath('.//span[@class="info-gray"]/text()').get()
            item["price"] = auto.xpath('.//span[@class="lever-price red"]/span/text()').get()
            item["auto_body"] = auto.xpath('.//ul[@class="lever-ul"]/li')[1].xpath('.//a/text()').get()
            engine = auto.xpath('.//ul[@class="lever-ul"]/li')[2].xpath('.//a/text()').getall()
            item["engine"] = ','.join(engine).strip(',')
            item["transmission"] = auto.xpath('.//ul[@class="lever-ul"]/li')[3].xpath('.//a/text()').get()
            item['auto_img'] = auto.xpath('.//div[@class="list-cont-img"]/a/img/@src').get()
            yield item

            