# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
#保证可以向oracle数据库中更新中文
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
class ZlzpSxPipeline(object):
    def process_item(self, item, spider):
        #连接oracle数据库
        conn=pymysql.connect(host='192.168.3.232',user='zwj',passwd='123456',db='caiji',charset='utf8',port=3306)
        cursor = conn.cursor()

        #在数据库中添加数据,若违反了唯一性约束则不插入
        sql_insert = "insert into ZPAH_SX(position,company,position_add,sitename,siteurl,gettime,area,zwyx,fbrq,gzjy,zprs,gzxz,zdxl,zwlb" \
                     ",gsgm,gsxz,gshy,gsfl,gszy) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                     "'%s','%s','%s','%s','%s','%s')"% (item['position'],item['company'],item['posAdd'],
                   item['sitename'],item['siteurl'],
                    item['gettime'],item['area'], item['zwyx'],  item['fbrq'],
                     item['gzjy'],  item['zprs'], item['gzxz'],  item['zdxl'],
                     item['zwlb'], item['gsgm'],  item['gsxz'],  item['gshy'],
                    item['gsfl'], item['gszy'])
        cursor.execute(sql_insert)

        conn.commit()

        #断开数据库的连接
        cursor.close()
        conn.close()
        return item
