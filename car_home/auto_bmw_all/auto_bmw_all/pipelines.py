# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib 
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class AutoBmwAllPipeline(object):
    def process_item(self, item, spider):
        return item

class BmwImagesPipeline(ImagesPipeline):
        
    def get_media_requests(self, item, info):
        img_url_list = item['image_urls']
        for img_url in img_url_list:
            yield Request(img_url,meta={'image_file':item['image_file']},)
    
    def file_path(self, request, response=None, info=None):
        image_file = request.meta['image_file']
        name = request.url.split('_')[-1]
        return '%s/%s.png'%(image_file,name)
    
    def item_completed(self, results, item, info):
        print(results)
        return item
