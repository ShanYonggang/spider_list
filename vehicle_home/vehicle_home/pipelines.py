# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import pymysql


class VehicleHomePipeline:
    def __init__(self):
        self.connect = pymysql.connect(
                                    host='123.57.40.204', user='root',
                                    password='syg7810354.', db='Spider',
                                    port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print("----------开启数据库存储模式----------------")
        self.connect.ping(reconnect=True)
        sql = 'insert into vehicle_home(usercont, vehicle_style, vehicle_by_location, vehicle_seller, vehcle_seller_date, vehicle_seller_money, vehicle_status, vehicle_evaluate,vehicle_bu_aim,evalute_date,evalute_title,visit_count,helpful_count,comment_count,evalute_infos) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(sql, (item["usercont"], ";".join(item["vehicle_style"]), item['vehicle_by_location'], item['vehicle_seller'], item['vehcle_seller_date'], "".join(item['vehicle_seller_money']), " ".join(item['vehicle_status']), " ".join(item['vehicle_evaluate']), " ".join(item['vehicle_bu_aim']), item['evalute_date'], item['evalute_title'], item['visit_count'], item['helpful_count'], item['comment_count'], item["evalute_infos"]))
        # test_sql = 'insert into test_sql(infos) values (%s)'
        # self.cursor.execute(test_sql, item["evalute_infos"])
        self.connect.commit()
        return item

    def close_spider(self, spider):
        print('----------关闭数据库资源-----------')
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.connect.close()
