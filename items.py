# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item,Field

class ZlzpSxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    position = Field()
    company =Field()
    posAdd =Field()
    sitename = Field()
    siteurl = Field()
    isyyzz = Field()
    gettime = Field()
    phone = Field()
    area = Field()
    #新增
    zwyx = Field()#职位月薪
    fbrq = Field()#发布日期
    gzjy = Field()#工作经验
    zprs = Field()#招聘人数
    gzxz = Field()#工作性质
    zdxl = Field()#最低学历
    zwlb = Field()#职位类别
    gsgm = Field()#公司规模
    gsxz = Field()#公司性质
    gshy = Field()#公司行业
    gsfl = Field()#公司福利 职位下面的小标签
    gszy = Field()#公司主页
    pass

