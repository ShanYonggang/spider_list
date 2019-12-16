import requests
from lxml import etree
import time
import multiprocessing
import pymysql

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'cookie': '_zap=47e250c3-7a07-41d6-88a7-52b3cb282921; d_c0="ALCvK5ioexCPTmjktJFsrBEH1LQX-TTUjkM=|1575956493"; capsion_ticket="2|1:0|10:1576116250|14:capsion_ticket|44:ZTEwNjMxZmQ0OTA4NDU5MGI1MWNiODgxYjg4MTRmMWE=|ac6c9175199323ab564e53969f64440ccc244feacfdf40e5bce5a8084d82a806"; z_c0="2|1:0|10:1576116298|4:z_c0|92:Mi4xRi1ac0JnQUFBQUFBc0s4cm1LaDdFQ2NBQUFDRUFsVk5TaTBaWGdBX2puWUIxcmhYa3hoR1hsWkRwN2FKOENGNDN3|7f3436a96ccb3cdf3d549b20ed658d14ab8c9b1f75937684fd3ee524fb061e93"; q_c1=f254b825456c428fb665bc0ba903aca4|1576116327000|1576116327000; __utma=51854390.997463445.1576214466.1576214466.1576214466.1; __utmz=51854390.1576214466.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100--|2=registration_date=20171105=1^3=entry_date=20171105=1; _xsrf=f03ebad1-fe74-45e4-a8e1-33c0c0219444; tshl=; tst=h; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576218531,1576221535,1576472582,1576482250; tgw_l7_route=64ba0a179156dda09fec37a3b2d556ed; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576483496'
}
url = 'https://www.zhihu.com/hot'
def get_question_num(url,headers):
    response = requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    reslut = html.xpath("//section[@class='HotItem']")
    # 获取问题的ID
    question_list = []
    for question in reslut:
        number = question.xpath(".//div[@class='HotItem-index']//text()")[0].strip()
        title = question.xpath(".//h2[@class='HotItem-title']/text()")[0].strip()
        href = question.xpath(".//div[@class='HotItem-content']/a/@href")[0].strip()
        question_num = href.split('/')[-1]
        question_list.append([question_num,title])
        # print(number,'\n',title,'\n',href)
    return question_list
# 数据json请求（问题均通过ajax请求）
# 分析链接格式,如下:
# https://www.zhihu.com/api/v4/questions/359056618/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=5&platform=desktop&sort_by=default
# 变化量如：question_id , offset=5,10,15......
def data_json_request(question_id,question_title,headers):
    num = 0
    i = 1
    while True:
        json_url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'.format(num)
        data_json = requests.get(json_url,headers=headers)
        all_detail_data = data_json.json()['data']
        length_detail_data = len(all_detail_data)
        for one_detail_data in all_detail_data:
            question_title = question_title
            answer_author = one_detail_data['author']['name']
            author_introduce = one_detail_data['author']['headline']
            author_followers = one_detail_data['author']['follower_count']
            answer_vote_num = one_detail_data['voteup_count']
            answer_comment_num = one_detail_data['comment_count']
            updated_time = one_detail_data['updated_time']
            content = one_detail_data['content']
            # 保存数据至数据库
            db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider_data')
            cursor = db.cursor()
            sql = 'INSERT INTO zhihu_hot_question(question_title,author_name,author_introduce,author_followers,answer_vote_num,answer_comment_num,updated_time,content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            try:
                if int(answer_vote_num) >= 90:
                    cursor.execute(sql,(question_title,answer_author,author_introduce,author_followers,answer_vote_num,answer_comment_num,updated_time,content))
                    db.commit()
                    print('数据写入成功！！！')
                else:
                    print('点赞数太少，不保存至数据库！！！')
            except:
                print('数据写入失败！')
                db.rollback()
            # print(question_title,'\n',answer_author,'\n',author_introduce,'\n',author_followers,'\n',answer_vote_num,'\n',answer_comment_num
            # ,'\n',updated_time,'\n',content)
        num = i*5
        i = i+1
        if length_detail_data == 0:
            print('answaer_stop!!!!!')
            break

# def save_to_mysql():
#     db = pymysql.connect(host='localhost',user='root',password='123456',port=3306,db='spider_data')
#     cursor = db.cursor()
#     sql = 'INSERT INTO zhihu_hot_question(question_title,author_name,author_introduce,author_followers,answer_vote_num,answer_comment_num,updated_time,content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    

def main():
    question_id = get_question_num(url,headers)
    print(question_id)
    print('当前环境CPU核数是：{}核'.format(multiprocessing.cpu_count()))
    p = multiprocessing.Pool(4)
    for q_id in question_id:
        p.apply_async(data_json_request,args=(q_id[0],q_id[1],headers))
    p.close()
    p.join()

if __name__ == "__main__":
    start = time.time()
    main()
    print('总耗时：%.5f秒'% float(time.time()-start))