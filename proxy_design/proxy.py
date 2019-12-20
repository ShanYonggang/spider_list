import requests
from lxml import etree
from connect_redis import r
import multiprocessing

class proxy():
    def __init__(self):
        self.key = 'proxy'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36'
        }
        self.proxy_list = []
        self.url = [ 'http://www.66ip.cn/{}.html'.format(i) for i in range(20)]

    def getContent(self):
        '''
        获取网站源代码
        :return:
        '''
        # url = 'http://www.66ip.cn/1.html'
        # 由于一页仅有5个代理IP，因此默认获取20页
        for url in self.url:
            data = requests.get(url, headers=self.headers)
            content = data.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(data.text)[0])
            self.parse(content)

    def parse(self,content):
        '''
        解析网站源代码
        :return:
        '''
        html = etree.HTML(content)
        reslut = html.xpath("//div[@align='center']/table/tr")[1:]
        for re in reslut:
            proxy_ip = re.xpath("./td/text()")[0]
            proxy_port = re.xpath("./td/text()")[1]
            proxy_address = re.xpath("./td/text()")[2]
            proxy_style = re.xpath("./td/text()")[3]
            proxy_check_time = re.xpath("./td/text()")[4]
            # 将获取的代理存放至列表中
            self.proxy_list.append(proxy_ip+'+'+proxy_port+'+'+proxy_address+'+'+proxy_style+'+'+proxy_check_time)
            proxy_value = proxy_ip+":"+proxy_port
            print(proxy_value)
            # 将代理添加至redis数据库中
            r.add(proxy_value)
    
    def get_proxy_random(self):
        '''
        随机获取代理地址
        :return:
        '''
        # 通过其是否可以访问百度验证其有效性
        url = 'https://www.baidu.com'
        value = r.random()
        print(value)
        if value is None:
            self.getContent()
        proxies = {"http": "http://" + value.decode("utf-8")}
        print(proxies)
        try:
            data = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=5)
            if data.status_code is not 200:
                print('代理无效，进行删除')
                r.delete(value)
                self.random()
            else:
                print('可以访问百度网页！有效代理')
                return 'http://' + value.decode("utf-8")
        except:
            print('代理无效，进行删除')
            r.delete(value)
            self.random()

proxy = proxy()
# ip = proxy.get_proxy_random()
# print(ip)

