from urllib import request,error 
from lxml import etree
import os
import time

class Get_PPT():

    def __init__(self):

        self.base_url = 'http://www.1ppt.com'
        self.page_url = 'ppt_dabian_{}.html'.format(1)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    # 获取进入ppt详细介绍页面的url   
    def get_urls(self,url):
        req = request.Request(url, headers=self.header)
        response = request.urlopen(req)
        text = response.read().decode('gb2312')
        html = etree.HTML(text)
        # 获取进入ppt详细介绍页面的url
        detail_url = html.xpath("//ul[@class='tplist']//h2/a/@href")
        ppt_urls = []
        for url in detail_url:
            ppt_urls.append(self.base_url+url)
        return ppt_urls
    # 获取详细页面中PPT下载的链接
    def get_down_ppt_url(self,url,file_name):
        ppt_urls = self.get_urls(url)
        for url in ppt_urls:
            print("下载链接为{}的ppt模板".format(url))
            req = request.Request(url, headers=self.header)
            response = request.urlopen(req)
            text = response.read().decode('gb2312')
            html = etree.HTML(text)
            name = html.xpath("//div[@class='ppt_info clearfix']/h1/text()")[0]
            down_url = html.xpath("//ul[@class='downurllist']//a/@href")[0]
            try:
                time.sleep(1)
                spon = request.urlopen(down_url)
                filename = file_name + '/' + '{}.zip'.format(name)
                with open(filename,"wb") as code:
                    code.write(spon.read())
            except error.HTTPError:
                print("403 Forbidden!!!!")
if __name__ == "__main__":
    ppt = Get_PPT()
    # 获取论文答辩模块的PPT模板（可根据自己需求更改、此时页数也需要根据此模块的情况进行修改）
    for i in range(1,9):
        print("下载第{}页的PPT".format(i))
        lunwen_url = '/xiazai/dabian/ppt_dabian_{}.html'.format(i)
        file_name = "第{}页PPT总和".format(i)
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        url = ppt.base_url + lunwen_url
        ppt.get_down_ppt_url(url,file_name)