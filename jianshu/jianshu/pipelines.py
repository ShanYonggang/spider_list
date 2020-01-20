# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JianshuPipeline(object):
    def __init__(self):
        params = {
            'host':'localhost',
            'user':'root',
            'password':'pass4321',
            'port':3306,
            'db':'jianshu',
            'charset':'utf8'
        }
        self.db = pymysql.connect(**params)
        self.cursor = self.db.cursor()
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''INSERT INTO article (title,author,pub_time,word_num,read_num,content,comment_num,support_num,process_url,article_id,origin_url,tags)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['author'],item['time'],item['word_num'],item['read_num'],item['content'],item['comment_num'],item['support_num'],item['process_url'],item['article_id'],item['origin_url'],item['tags']))
        self.db.commit()
        return item
