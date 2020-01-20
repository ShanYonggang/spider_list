# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['httpbin.org/']
    start_urls = ['http://httpbin.org/']

    def parse(self, response):
        print(response['headers'])
