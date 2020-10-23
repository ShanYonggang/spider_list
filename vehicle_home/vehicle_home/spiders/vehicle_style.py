import scrapy
from vehicle_home.items import VehicleHomeItem
import re


class VehicleStyleSpider(scrapy.Spider):
    name = 'vehicle_style'
    allowed_domains = ['k.autohome.com.cn']
    start_urls = ['https://k.autohome.com.cn/suva01/']

    def parse(self, response):
        # 获取车型级别链接
        vehicle_style_url = response.xpath("//div[@class='findcont-choose']/a/\
                                            @href").getall()
        # 获取车型级别下属所有车型的链接
        vehicle_style_one_url = response.xpath("//ul[@class='list-cont']/li/div\
                                        [@class='cont-pic']/a/@href").getall()
        # yield {
        #     "vehicle_style_one_url": vehicle_style_one_url,
        #     # "vehicle_style_url": vehicle_style_url
        # }
        if vehicle_style_url is not None:
            for url in vehicle_style_url:
                yield response.follow(url, self.parse)
        if vehicle_style_one_url is not None:
            for url in vehicle_style_one_url:
                yield response.follow(url, self.parse_vehicle_detail)

    def parse_vehicle_detail(self, response):
        # 每个用户评价的口碑详细信息
        kou_bei_detail_url = response.xpath("//div[@class='allcont border-b-solid']\
                                        //a/@href").getall()
        # 下一页链接
        kou_bei_next_url = response.xpath("//div[@class='page']//a[@class=\
                                        'page-item-next']/@href").get()
        # yield {
        #     "kou_bei_detail_url": kou_bei_detail_url,
        # }
        if kou_bei_detail_url is not None:
            for url in kou_bei_detail_url:
                yield response.follow(url, self.parse_vehicle_detail_infos)
        if kou_bei_next_url is not None:
            yield response.follow(kou_bei_next_url, self.parse_vehicle_detail)

    def parse_vehicle_detail_infos(self, response):
        item = VehicleHomeItem()
        # 获取用户昵称
        usercont = response.xpath("//div[@class='mouth']//dl[@class='user-cont']\
                                    //div[@class='user-name']//a/text()").get()
        # 车型
        vehicle_style = response.xpath("//div[@class='choose-con']//dl//dd//a/\
                                        text()").getall()
        # 购车情况
        choose_dl = response.xpath("//div[@class='choose-con']//dl")
        info_length = len(choose_dl)
        # 购车地点
        vehicle_by_location = choose_dl[1].xpath("./dd//text()").get()
        # 购车所属品牌
        vehicle_seller = choose_dl[2].xpath("./dd/a/text()").get()
        # 购车时间\价格
        if vehicle_seller is not None:
            vehcle_seller_date = choose_dl[3].xpath("./dd/text()").get()
            vehicle_seller_money = choose_dl[4].xpath("./dd//text()").getall()
        else:
            vehcle_seller_date = choose_dl[2].xpath("./dd/text()").get()
            vehicle_seller_money = choose_dl[3].xpath("./dd//text()").getall()
        # 油耗或着电耗，目前行驶里程
        vehicle_status = choose_dl[-10].xpath("./dd/p//text()").getall()
        # 购车多个方面的评价
        vehicle_evaluate = response.xpath("//span[@class='testfont']/\
                                            text()").getall()
        # 购车目的
        vehicle_bu_aim = choose_dl[-1].xpath(".//dd/p/text()").getall()
        # 发布口碑的时间
        evalute_date = response.xpath("//div[@class='mouth-item koubei-final']//\
                        div[@class='title-name name-width-01']/b/text()").get()
        # 口碑题目
        evalute_title = response.xpath("//div[@class='mouth-item koubei-final']//\
                        div[@class='kou-tit']/h3/text()").get()
        # 发布的内容
        evalute_infos = response.xpath("//div[@class='mouth-item koubei-final']//\
                        div[@class='text-con']//text()").getall()
        # 浏览量
        visit_count = response.xpath("//div[@class='mouth-remak']//div[@class=\
                                'help']//span[@class='orange']/text()").get()
        # 口碑支持数
        helpful_count = response.xpath("//div[@class='mouth-remak']//div[@class=\
                        'help']//label[@class='supportNumber']/text()").get()
        # 评论数
        comment_count = response.xpath("//div[@class='mouth-remak']//div[@class=\
                        'help']/a//span/text()").get()

        # item["info_length"] = info_length
        item["usercont"] = usercont
        item["vehicle_style"] = vehicle_style
        item["vehicle_by_location"] = re.sub("[A-Za-z0-9\!\%\[\]\,\。\(\)\}\{\_\=\;&''+\<\>//$.::\"-#：\- \r\n]", "", "".join(vehicle_by_location))
        # 经销商信息爬取时候获取不到数据
        item["vehicle_seller"] = vehicle_seller
        item["vehcle_seller_date"] = vehcle_seller_date
        item["vehicle_seller_money"] = vehicle_seller_money
        item["vehicle_status"] = vehicle_status
        item["vehicle_evaluate"] = vehicle_evaluate
        item["vehicle_bu_aim"] = vehicle_bu_aim
        item["evalute_date"] = evalute_date
        item["evalute_title"] = evalute_title
        item["evalute_infos"] = re.sub("[A-Za-z0-9\!\%\[\]\,\。\(\)\}\{\_\=\;&''+\<\>//$.::\"-#：\- \r\n]", "", "".join(evalute_infos))
        item["visit_count"] = visit_count
        item["helpful_count"] = helpful_count
        item["comment_count"] = comment_count
        # yield {
        #     "info_length": info_length,
        #     "usercont": usercont,
        #     "vehicle_style": vehicle_style,
        #     "vehicle_by_location": vehicle_by_location,
        #     "vehicle_seller": vehicle_seller,
        #     "vehcle_seller_date": vehcle_seller_date,
        #     "vehicle_seller_money": vehicle_seller_money,
        #     "vehicle_status": vehicle_status,
        #     "vehicle_evaluate": vehicle_evaluate,
        #     "vehicle_bu_aim": vehicle_bu_aim,
        #     "evalute_date": evalute_date,
        #     "evalute_title": evalute_title,
        #     # "evalute_infos": evalute_infos,
        #     "visit_count": visit_count,
        #     "helpful_count": helpful_count,
        #     "comment_count": comment_count,
        # }
        return item
