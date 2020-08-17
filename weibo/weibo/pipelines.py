# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb


class WeiboPipeline(object):
    def process_item(self, item, spider):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db="scrapy",
                             charset='utf8')
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        # 使用 fetchone() 方法获取一条数据
        sql = "insert into fans_yyqx (id, name, follow_count, followers_count) value({id},'{name}',{follow_count},{followers_count})".format(
            id=item["id"],
            name=item["name"],
            follow_count=item["follow_count"],
            followers_count=item["followers_count"])
        try:
            cur.execute(sql)
            db.commit()
        except:
            debug("dumplicate {sql}".format(sql=sql))
            db.rollback()
        # 关闭数据库连接
        db.close()
        return item
def debug(param):
    print('\033[0;36m {param} \033[0m'.format(param=param))