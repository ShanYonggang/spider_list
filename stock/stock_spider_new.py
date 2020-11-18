# -*- coding:UTF-8 -*-
"""
 * @Author: Jack Shan
 * @Date: 2020-11-17 14:20:17
 * @Last Modified by:   Jack Shan
 * @Last Modified time: 2020-11-17 14:20:17
"""
# 相关库的导入
import requests
import pymysql
from lxml import etree
import pandas as pd
import threading
import time
import datetime
import random
from queue import Queue
import logging
import os


# 添加日志相关内容
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
# 创建handler，用于写入日志文件
file = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/stock/Logs/'
log_name = log_path + file + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode="w", encoding="UTF-8")
fh.setLevel(logging.DEBUG)    # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] -\
                                %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)
# 定义日志


class CrwalStockName(threading.Thread):

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 \
        Safari/537.36"
    }

    def __init__(self, page_queue, stock_name, *args, **kwargs):
        super(CrwalStockName, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.stock_name = stock_name

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            if "funds" not in url:
                self.parse_page(url)
            else:
                self.parse_page_detail(url)

    def parse_page(self, url):
        try:
            # logger.info('{}网页解析完成'.format(url))
            response = requests.get(url=url, headers=self.headers)
            html = etree.HTML(response.text)
            text1 = "".join(html.xpath("//div[@id='history_funds_analysis_free']\
                                        //p//text()"))
            text2 = html.xpath("//p[@class='zjlxlstj_txt mb14']//\
                               text()")[0].strip()
            text = text1 + "&" + text2
            stock_id = str(url).split("/")[-2]
            date = datetime.datetime.now()
            today = "{}/{}/{}".format(date.year, date.month, date.day)
            self.stock_name.put((text, stock_id, today))
            time.sleep(random.randint(1, 2))
        except(Exception):
            logger.info('{}网页解析失败'.format(url))
            self.page_queue.put(url)

    def parse_page_detail(self, url):
        try:
            # logger.info('{}网页解析完成'.format(url))
            response = requests.get(url=url, headers=self.headers)
            html = etree.HTML(response.text)
            data = html.xpath("//div[@id='history_table_free']//tr")[2:]
            stock_id = str(url).split("/")[-3]
            for i in data:
                date = tuple(i.xpath(".//td//text()"))
                value = (stock_id, date[0], date[1], date[2], date[3], date[4],
                         date[5], date[6], date[7], date[8], date[9], date[10])
                self.stock_name.put(value)
                time.sleep(random.randint(1, 2))
        except(Exception):
            logger.info('{}网页解析失败'.format(url))
            self.page_queue.put(url)


class StockNameConsumer(threading.Thread):

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 \
        Safari/537.36"
    }

    sql_recode = []

    def __init__(self, page_queue, stock_name, connect, *args, **kwargs):
        super(StockNameConsumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.stock_name = stock_name
        self.connect = connect

    def run(self):
        while True:
            if self.stock_name.empty():
                if self.page_queue.empty():
                    return
            data = self.stock_name.get()
            print(data)
            if len(data) == 3:
                self.save_data(data)
            else:
                self.save_data_detail(data)

    def save_data(self, data):
        try:
            print(data[0], data[1])
            self.connect.ping(reconnect=True)
            # sql = "update stock_name_new_copy2 set text = '{}' where id = {}"
            # .format(data[0], data[1])
            sql = "insert into stock_name_new_copy3(text, id, date) values (%s, \
                    %s, %s)"
            cursor = self.connect.cursor()
            cursor.execute(sql, tuple(data))
            self.connect.commit()
        except(Exception):
            logger.error('{}数据保存数据库失败'.format(data))

    def save_data_detail(self, data):
        try:
            # logger.info('{}数据保存完成'.format(data))
            self.connect.ping(reconnect=True)
            sql = "insert into stock_price_new_copy3(id, tr_time, end_price, \
            up_down, money_in, d5_in_big, b_money, b_part, m_money, m_part,\
            l_money, l_part) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s)"
            cursor = self.connect.cursor()
            cursor.execute(sql, data)
            self.connect.commit()
        except(Exception):
            logger.error('{}数据保存数据库失败'.format(data))


def main():
    connect = pymysql.connect(host='xxxxx', user='root', password='\
                                xxxxx', port=3306, db='stock')
    page_queue = Queue()
    stock_name = Queue()
    stock_id = pd.read_sql(sql='select distinct stock_id from All_Stock_Name',
                           con=connect)
    stock_list = list(stock_id["stock_id"])
    for i in stock_list:
        text_url = "http://stockpage.10jqka.com.cn/"+i+"/"
        detail_url = "http://stockpage.10jqka.com.cn/"+i+"/funds/"
        page_queue.put(text_url)
        page_queue.put(detail_url)

    for i in range(2):
        t = CrwalStockName(page_queue=page_queue, stock_name=stock_name)
        t.start()

    for i in range(3):
        t = StockNameConsumer(page_queue=page_queue, stock_name=stock_name,
                              connect=connect)
        t.start()


if __name__ == "__main__":
    main()
