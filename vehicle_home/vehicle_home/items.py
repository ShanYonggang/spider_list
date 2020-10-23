# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VehicleHomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # info_length = scrapy.Field()
    usercont = scrapy.Field()
    vehicle_style = scrapy.Field()
    vehicle_by_location = scrapy.Field()
    vehicle_seller = scrapy.Field()
    vehcle_seller_date = scrapy.Field()
    vehicle_seller_money = scrapy.Field()
    vehicle_status = scrapy.Field()
    vehicle_evaluate = scrapy.Field()
    vehicle_bu_aim = scrapy.Field()
    evalute_date = scrapy.Field()
    evalute_title = scrapy.Field()
    evalute_infos = scrapy.Field()
    visit_count = scrapy.Field()
    helpful_count = scrapy.Field()
    comment_count = scrapy.Field()
