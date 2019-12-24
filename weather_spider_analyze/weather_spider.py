from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import datetime
import pymysql

url = 'http://tianqi.2345.com/wea_history/54511.htm'
driver=webdriver.Chrome("E:/0_软件/chromedriver.exe")
try:
    driver.get(url)
    time.sleep(2)
    print(driver.current_url)
    # 暂时获取24页(5年的信息)
    for i in range(60):
        weathter_lists = driver.find_elements_by_xpath('//table/tbody/tr')
        for weather in weathter_lists:
            infos = weather.find_elements_by_tag_name('td')
            weather_time = infos[0].text[:-3]   # 时间
            # 将字符串时间转换成Datetime
            weather_time = datetime.datetime.strptime(weather_time,'%Y-%m-%d').date()
            high_tm = infos[1].text  # 最高温
            low_tm = infos[2].text  # 最低温
            weath = infos[3].text   # 天气
            wind_style = infos[4].text   # 风向、风力
            air = infos[5].text  # 空气质量指数
            db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider_data')
            cursor = db.cursor()
            sql = 'INSERT INTO weather_beijing(weather_time,high_tem,low_tem,weather,wind_direction,air) VALUES(%s,%s,%s,%s,%s,%s)'
            try: 
                cursor.execute(sql,(weather_time,high_tm,low_tm,weath,wind_style,air))
                db.commit()
                print('数据保存成功!')
            except:
                print('数据保存失败!')
            print(weather_time,high_tm,low_tm,weath,wind_style,air)
        # 点击上一页
        pre_page_button = driver.find_element_by_xpath('//div[@id="prevNextBtn"]/a[@class="prev"]')
        pre_page_button.click()
        time.sleep(3)
except:
    print('fail!')
driver.close()