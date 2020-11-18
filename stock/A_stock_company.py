import requests
import pymysql
from lxml import etree
import time
import random


def crawl_stock_company(url, connect):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 \
            Safari/537.36"
    }
    data = requests.get(url, headers=headers).text
    html = etree.HTML(data)
    tr_data = html.xpath("//table[@id='myTable04']//tbody/tr")
    for tr in tr_data:
        stock_id = tr.xpath(".//td//text()")[1]
        stock_name = tr.xpath(".//td//text()")[2]
        company_name = tr.xpath(".//td//text()")[3]
        company_province = tr.xpath(".//td//text()")[4]
        company_loc = tr.xpath(".//td//text()")[5]
        company_num = tr.xpath(".//td//text()")[8]
        company_create_date = tr.xpath(".//td//text()")[9]
        company_trade = tr.xpath(".//td//text()")[-3]
        company_business = tr.xpath(".//td//text()")[-1]
        value = (stock_id, stock_name, company_name, company_province,
                 company_loc, company_num, company_create_date,
                 company_trade, company_business)
        sql = "insert into All_Stock_Name(stock_id, stock_name, \
                company_name, company_province, company_loc, company_num, \
                company_create_date,company_trade, company_business) values \
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = connect.cursor()
        cursor.execute(sql, value)
        connect.commit()
        print(value)


if __name__ == "__main__":
    connect = pymysql.connect(host='xxxxx', user='root', password=
                              'xxxxxx', port=3306, db='stock')
    file = open("new_{}.text".format(time.time()), "w")
    for i in range(1, 207):
        try:
            url = "https://s.askci.com/stock/a/0-0?reportTime=2020-03-31&pageNum={}#\
                    QueryCondition".format(i)
            crawl_stock_company(url, connect)
            time.sleep(random.randint(1, 2))
        except(Exception):
            print("股票抓取失败！！！")
            file.write("股票{}数据未抓取成功!".format(i)+"\n")
