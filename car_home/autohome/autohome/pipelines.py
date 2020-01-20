# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import pymysql

class AutohomePipeline(object):

    def __init__(self):
        self.fp = open('auto.json','a+',encoding='utf-8')

    def process_item(self, item, spider):
        file = json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(file)
        print(self.fp.read())
        return item

    def close_spider(self,spider):
        self.fp.close()
        print('Spider Stop...')

class MongoPipeline(object):
    
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print('Spider Start run...')

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
        print('Spider Stop...')

class MysqlPipeline(object):

    def __init__(self,host,port,user,password,db):
        self.host = host
        self.user = user
        self.password =password
        self.port = port
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(
            host = crawler.settings.get('HOST'),
            port = crawler.settings.get('PORT'),
            user = crawler.settings.get('USER'),
            password = crawler.settings.get('PASSWORD'),
            db = crawler.settings.get('DB'),
        )

    def open_spider(self,spider):
        self.db =  pymysql.connect(host=self.host,user=self.user,port=self.port,password=self.password,db=self.db,charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        sql = 'insert into auto_data (model_name,level,auto_body,price,engine,transmission,auto_img) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql,(item["model_name"],item["level"],item["price"],item["auto_body"],item["engine"],item["transmission"],item['auto_img']))
        self.db.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()