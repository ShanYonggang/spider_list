# -*- coding: utf-8 -*-
import scrapy
from auto_bmw.items import AutoBmwItem

class BmwSpiderSpider(scrapy.Spider):
    name = 'bmw_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/66.html']

    def parse(self, response):
        uibox_urls = response.xpath('//div[@class="uibox"]')[1:]
        for uibox_url in uibox_urls:
            item = AutoBmwItem()
            item['image_file'] = uibox_url.xpath('./div[@class="uibox-title"]/a')[0].xpath('./text()').get()
            image_urls = uibox_url.xpath('./div')[-1].xpath('.//img/@src').getall()
            item['image_urls'] = list(map(lambda url: response.urljoin(url),image_urls))
            yield item
