# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    word_num = scrapy.Field()
    read_num = scrapy.Field()
    content = scrapy.Field()
    comment_num = scrapy.Field()
    support_num = scrapy.Field()
    process_url = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    tags = scrapy.Field()
    pass
