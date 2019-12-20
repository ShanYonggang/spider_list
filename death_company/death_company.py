import requests 
from xici import proxy
import pymysql
import multiprocessing
import time
import random
import requests

def get_data(json_url,proxies):
    user_agent_list = [
        # Opera
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        # 360
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 淘宝浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        # 猎豹浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        # QQ浏览器
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        # sogou浏览器
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        # maxthon浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        # UC浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    ]
    UserAgent = random.choice(user_agent_list)
    # print(UserAgent)
    headers = {
        'User-Agent': UserAgent,
        'cookie': '_ga=GA1.2.1552320068.1576549906; _gid=GA1.2.2023492117.1576549906; gr_user_id=3d348e20-9820-49f1-afcb-8c55d72ad2d2; MEIQIA_TRACK_ID=1V5jsLMCkebhIrU4wdaptzAcxNh; MEIQIA_VISIT_ID=1V5jsNCG3mS1OZ381JMTk7aWSy4; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1576549906,1576553882,1576568223,1576574298; _gat_gtag_UA_59006131_1=1; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1576574523'
    }
    try:
        json_data = requests.get(json_url,headers=headers,proxies=proxies)
        if json_data.status_code is 200:
            deatail_infos = json_data.json()['data']['info']
            for data in deatail_infos:
                # 公司名称
                com_name = data['com_name']
                # 公司简介
                com_description = data['com_des']
                # 公司创建时间
                com_born = data['born']
                # 公司关闭时间
                com_change_close_date = data['com_change_close_date']
                # 公司类型
                com_style = data['cat_name'] + data['se_cat_name']
                # 公司地址
                com_position = data['com_prov']
                # 公司创始人
                com_team = data['com_team']
                com_people = ''
                for name in com_team:
                    com_people += name['name'] + '/' + name['per_des'] + ';'
                # 公司标签
                com_tag = data['com_tag']
                com_tags = ''
                for tag in com_tag:
                    com_tags += tag['tag_name'] + '/'
                # 投资轮次
                com_fund_status_name = data['com_fund_status_name']
                # 投资公司
                com_invst = data['com_invst']
                com_invsts = ''
                for com in com_invst:
                    com_invsts += com['invst_name'] + '/'
                # 公司死亡原因
                closure_type = data['closure_type']
                death_reason = ''
                for da in closure_type:
                    death_reason += da['name'] + '/'
                # 公司存活时间
                live_time = data['live_time']
                # 公司资金情况
                total_money = data['total_money']
                # 公司类型
                cat_name = data['cat_name']
                db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider_data')
                cursor = db.cursor()
                sql = 'INSERT INTO juzi_death_company_all_info(com_name,com_description,com_born,com_change_close_date,com_style,com_position,com_people,com_tags,com_fund_status_name,com_invsts,death_reason,live_time,total_money,cat_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                try:
                    cursor.execute(sql,(com_name,com_description,com_born,com_change_close_date,com_style,com_position,com_people,com_tags,com_fund_status_name,com_invsts,death_reason,live_time,total_money,cat_name))
                    db.commit()
                    print('{}数据写入成功！！！'.format(com_name))
                except:
                    print('数据写入失败！')
                    db.rollback()
        else:
            print('{}访问不了了！！！'.format(json_url))
    except:
        print("{}数据爬取失败".format(json_url))

if __name__ == "__main__":
    start = time.time()
    print('当前环境CPU核数是：{}核'.format(multiprocessing.cpu_count()))
    json_urls = [ 'https://www.itjuzi.com/api/closure?com_prov=&sort=&page={}&keyword=&cat_id='.format(i) for i in range(1,629)]
    p = multiprocessing.Pool(4) 
    i = 1
    proxies = proxy.get_proxy_random()
    for json_url in json_urls:
        if (i%35 == 0):
            proxy.get_proxy_random()
        p.apply_async(get_data,args=(json_url,proxies,))
        i += 1
    p.close()
    p.join()
    print('总耗时：%.5f秒'% float(time.time()-start))