# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    model_name = scrapy.Field()
    level = scrapy.Field()
    auto_body = scrapy.Field()
    price = scrapy.Field()
    engine = scrapy.Field()
    transmission = scrapy.Field()
    auto_img = scrapy.Field()
