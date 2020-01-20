# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ["jianshu.com"]
    start_urls = ["https://www.jianshu.com/"]
    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        author = response.xpath('//span[@class="_22gUMi"]/text()').get()
        time = response.xpath('//div[@class="s-dsoj"]/time/text()').get()
        word_num = response.xpath('//div[@class="s-dsoj"]/span/text()').getall()[0].split(' ')[-1]
        read_num = response.xpath('//div[@class="s-dsoj"]/span/text()').getall()[1].split(' ')[-1]
        content = response.xpath('//article[@class="_2rhmJa"]').get()
        comment_num = response.xpath('//div[@class="-pXE92"]//span/text()').getall()[1]
        support_num = response.xpath('//div[@class="-pXE92"]//span/text()').getall()[-1]
        process_url = response.url.split('?')[0]
        article_id = process_url.split('/')[-1]
        tags = response.xpath('//div[@class="_2Nttfz"]/a//span/text()').getall()
        tags = ','.join(tags)
        origin_url = response.url
        item = JianshuItem(title=title,author=author,time=time,word_num=word_num,read_num=read_num,
        content=content,comment_num=comment_num,support_num=support_num,process_url=process_url,article_id=article_id,
        origin_url=origin_url,tags=tags)
        return item
