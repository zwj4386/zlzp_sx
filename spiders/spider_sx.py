#!/usr/bin/python
# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from ..items import ZlzpSxItem
import re
import os
import time
import sys
import pymysql
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class ZhaoPinSpider(Spider):
    name = "zlzp_sx"
    allowed_domains = ["jobs.zhaopin.com"]
    #智联招聘，已选城市贵州省
    start_urls = [
        "http://jobs.zhaopin.com/shanxi/",
        "http://jobs.zhaopin.com/taiyuan/",
        "http://jobs.zhaopin.com/datong/",
        "http://jobs.zhaopin.com/yangquan/",
        "http://jobs.zhaopin.com/changzhi/",
        "http://jobs.zhaopin.com/jincheng/",
        "http://jobs.zhaopin.com/shuozhou/",
        "http://jobs.zhaopin.com/jinzhong/",
        "http://jobs.zhaopin.com/yuncheng/",
        "http://jobs.zhaopin.com/xinzhou/",
        "http://jobs.zhaopin.com/linfen/",
        "http://jobs.zhaopin.com/lvliang/",
        "http://jobs.zhaopin.com/yongji/"
    ]
    def Address(self,response):
        try:
            hxs = Selector(response)
            item = ZlzpSxItem()

            #8/21编写

            zwyx=hxs.xpath('//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()
            item['zwyx']=''.join(zwyx)
            #发布日期
            fbrq=hxs.xpath('//span[@id="span4freshdate"]/text()').extract()
            fbrq = ''.join(fbrq)
            if fbrq=='0002-01-01 00:00:00':
                item['fbrq']=u'最新'
            else:
                item['fbrq']=fbrq
            #工作经验
            gzjy=hxs.xpath(u"//li[contains(span/text(),'工作经验')]/strong/text()").extract()
            item['gzjy'] = ''.join(gzjy)
            #zprs=Field()#招聘人数
            zprs = hxs.xpath(u"//li[contains(span/text(),'招聘人数')]/strong/text()").extract()
            item['zprs'] = ''.join(zprs)
            # gzxz=Field()#工作性质
            gzxz = hxs.xpath(u"//li[contains(span/text(),'工作性质')]/strong/text()").extract()
            item['gzxz'] = ''.join(gzxz)
            #zdxl=Field()#最低学历
            zdxl = hxs.xpath(u"//li[contains(span/text(),'最低学历')]/strong/text()").extract()
            item['zdxl'] =  ''.join(zdxl)
            #zwlb=Field()#职位类别
            zwlb = hxs.xpath(u"//li[contains(span/text(),'职位类别')]")
            zwlb = ''.join(zwlb.xpath('string(.)').extract())
            item['zwlb'] =  ''.join(zwlb)
            #div右边的
            div=hxs.xpath("//ul[@class='terminal-ul clearfix terminal-company mt20']")
            #gsgm=Field()#公司规模
            gsgm=div.xpath(u"./li[contains(span/text(),'公司规模')]/strong/text()").extract()
            item['gsgm'] =  ''.join(gsgm)
            #gsxz=Field()#公司性质
            gsxz = div.xpath(u"./li[contains(span/text(),'公司性质')]/strong/text()").extract()
            item['gsxz'] =  ''.join(gsxz)
            #gshy=Field()#公司行业
            gshyy = div.xpath(u"./li[contains(span/text(),'公司行业')]/strong")
            hshy = gshyy.xpath('string(.)').extract()
            item['gshy'] = ''.join(hshy)
            #gszy=Field()#公司主页
            gszy = div.xpath(u"./li[contains(span/text(),'公司主页')]/strong/a/@href").extract()
            item['gszy'] =  ''.join(gszy)
            #gsfl=Field()#公司福利 职位下面的小标签
            gsflList=hxs.xpath('//div[@class="welfare-tab-box"]/span/text()').extract()
            gsfl=' '.join(str(i) for i in gsflList)
            item['gsfl']=gsfl
            postionList = hxs.xpath('//div[@class="inner-left fl"]/h1/text()').extract()
            position = postionList[0]
            item['position'] = position
            companyList = hxs.xpath('//p[@class="company-name-t"]/a/text()').extract()
            company = companyList[0]
            item['company'] = company

            posAddList = hxs.xpath(u'//div[@class="company-box"]/ul/li[contains(span/text(),"公司地址")]')
            posAdd =posAddList.xpath('string(.)').extract()
            pos=''.join(posAdd).replace('\r\n','').replace(u'查看公司地图','').replace(" ","")
            item['posAdd'] = pos

            sitenameList = hxs.xpath('//div[@class="all_navcontent"]/a/@title').extract()
            sitename = sitenameList[0]
            item['sitename'] = sitename

            siteurl = str(response).strip('<200>').strip()
            item['siteurl'] = siteurl

            gettime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            item['gettime'] = gettime
            #有问题
            phoneList = hxs.xpath('//div[@class="tab-cont-box"]')
            content = phoneList.xpath('string(.)').extract()
            MobileList = []
            if phoneList == None:
                pass
            else:
                phone = re.findall('1\d{10}|0\d{3}-\d{8}|\d{8}', str(content).decode('unicode-escape'))
                for p in phone:
                    MobileList.append(p)
                else:
                    pass
            realPhone=' '.join(MobileList)
            item['phone'] = realPhone

            areaList = hxs.xpath('//div[@class="bread_crumbs"]/a[2]/strong/text()').extract()
            area = areaList[0][0:len(areaList[0])]
            if area:
                item['area'] = area
            else:
                item['area'] = None
            yield item
        except BaseException,e:
            print e
    #作用是 链接数据库，找到要存储的数据
    def parse(self, response):
        try:
            #链接数据库
            conn = pymysql.connect(host='192.168.3.232', user='zwj', passwd='123456', db='caiji', charset='utf8',
                                   port=3306)
            cursor = conn.cursor()
            hxs = Selector(response)
            #class=post为一条数据的选择器名称
            position_sites = hxs.xpath('//span[@class="post"]')
            #遍历所有的选择器
            for psite in position_sites:
                #a/@href 为什么这样写
                link = psite.xpath('a/@href').extract()
                url = link[0]
                sql_select = "select siteurl from ZPAH_SX where siteurl='%s'"%url
                cursor.execute(sql_select)
                #cursor.fetchall()返回True or False
                rs = cursor.fetchall()
                if rs:
                    pass
                else:
                    #返回？
                    yield Request(url,callback=self.Address)
            #链接到下一个地址
            urlnextList = hxs.xpath('//span[@class="search_page_next"]/a/@href').extract()
            if urlnextList:
                urlnext = "http://jobs.zhaopin.com" + urlnextList[0]
                yield Request(urlnext,callback = self.parse)
            #关闭数据库
            cursor.close()
            conn.close()
        except BaseException,e:
            print e
