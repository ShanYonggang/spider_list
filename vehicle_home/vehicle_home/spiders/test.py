import requests
from lxml import etree
import json


data = requests.get("https://k.autohome.com.cn/detail/view_01enhzwr4z6csk0c9j70r00000.html#pvareaid=2112108").text
html = etree.HTML(data).xpath("//div[@class='choose-con']//dl")
seller_id = html[2].xpath(".//a/@data-val")[0]
data_evalid = html[2].xpath(".//a/@data-evalid")[0]
url_api = "https://k.autohome.com.cn/frontapi/GetDealerInfor?dearerandspecIdlist=" + seller_id + "," + data_evalid +"|"
data = requests.get(url_api).text 

seller_name = json.loads(data)["result"]["List"][0]["CompanySimple"]
print(seller_id, data_evalid)

print(seller_name)
