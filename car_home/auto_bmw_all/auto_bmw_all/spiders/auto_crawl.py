# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from auto_bmw_all.items import AutoBmwAllItem

class AutoCrawlSpider(CrawlSpider):
    name = 'auto_crawl'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/66.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+/pic/series/66-.+'), callback='parse_item',follow=True),
    )

    src="//car3.autoimg.cn/cardfs/product/g1/M07/63/01/240x180_0_q95_autohomecar__ChsEmVz37-OABcHCAAR_DO3soxI667.jpg"
    src="//car3.autoimg.cn/cardfs/product/g1/M07/63/01/  800x0_1_q95_autohomecar__ChsEmVz37-OABcHCAAR_DO3soxI667.jpg"

    def parse_item(self, response):
        uibox = response.xpath('//div[@class="uibox"]')
        item = AutoBmwAllItem()
        item['image_file'] = uibox.xpath('./div[@class="uibox-title"]/text()').get()
        image_url = uibox.xpath('./div[@class="uibox-con carpic-list03 border-b-solid"]/ul/li//img/@src').getall()
        item['image_urls'] = list(map(lambda url: response.urljoin(url.replace('240x180_0','800x0_1')),image_url))
        yield item

        
