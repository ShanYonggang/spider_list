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

class AutoBmwPipeline(object):

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'image')
        if not os.path.exists(self.file_path):
            os.mkdir(self.file_path)
        else:
            print('Path already exist......')
        
    def process_item(self, item, spider):
        image_file = item['image_file']
        image_urls = item['image_urls']
        image_path = os.path.join(self.file_path,image_file)
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        for url in image_urls:
            image_name = url.split('__')[-1]
            urllib.request.urlretrieve(url,os.path.join(image_path,image_name))
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

    