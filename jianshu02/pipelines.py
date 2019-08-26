# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import connect
from twisted.enterprise import adbapi #这个模块专门进行数据库处理的
from pymysql import cursors
"""
    1 open_spider和close_spider 的使用
        作为一个下载中间件，可以在__init__的方法中做一些初始化的操作，
        也可以在open_spider中进行一些初始化操作，它是在爬虫开始时执行的方法，且执行一次
        可以在close_spider中执行一些关闭的操作，它是在爬虫结时执行的方法，且执行一次
    
    2 在进行数据数据库连接的时候
            可以这样做：
                self.mysqlConn = connect(host="",port="")
            也可以这样做
                self.mysqlConn = connect(**self.dbParams)
                
    3 保存到数据库的异步操作，from twisted.enterprise import adbapi
        （1） pool的建立
        （2） defer.addErrback 添加错误处理方法
        
"""
#----------------------------------同步插入数据库---------------------
class Jianshu02Pipeline(object):

    # def __init__(self):
    #     self.dbParams = {
    #         "host":"127.0.0.1",
    #         "user":"root",
    #         "password":"123456",
    #         "database":"test",
    #         "port":3306,
    #         "charset":"utf8"
    #     }
    #     self.mysqlConn = connect(**self.dbParams)
    #     self.cursor = self.mysqlConn.cursor()
    #     self._insertSql = None

    def open_spider(self,spider):
        print("执行pipeline----open_spider")
        self.dbParams = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "123456",
            "database": "test",
            "port": 3306,
            "charset": "utf8"
        }
        self.mysqlConn = connect(**self.dbParams)
        self.cursor = self.mysqlConn.cursor()
        self._insertSql = None

    def close_spider(self,spider):
        print("执行pipeline----close_spider")
        self.cursor.close()
        self.mysqlConn.close()


    @property
    def insertSql(self):
        if not self._insertSql:
            self._insertSql = """
                insert into jianshu(articleid,url,content,title,author,publicdate,text_num,read_num,comment_num,like_num,cated,stars) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._insertSql
        return self._insertSql

    def process_item(self, item, spider):
        try:
            self.cursor.execute(self.insertSql,(item["articleid"],item["url"],item["content"],item["title"],
                                                item["author"], item["publicdate"], item["text_num"], item["read_num"],
                                                item["comment_num"], item["like_num"], item["cated"], item["stars"]))

            self.mysqlConn.commit()

        except Exception as e:
            print("e============"+str(e.args))


#-------------------------异步插入数据库---------------------------


class JianShuTwistedPipeline(object):

    #刚开始执行爬虫的时候执行
    def open_spider(self,spider):
        print("执行pipeline----open_spider")
        self.dbParams = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "123456",
            "database": "test",
            "port": 3306,
            "charset": "utf8",
            "cursorclass":cursors.DictCursor
        }

        #创建一个连接池
        self.dbpool = adbapi.ConnectionPool("pymysql",**self.dbParams)
        self._insertSql = None

    #赋值insertSql语句
    @property
    def insertSql(self):
        if not self._insertSql:
            self._insertSql = """
                    insert into jianshu(articleid,url,content,title,author,publicdate,text_num,read_num,comment_num,like_num,cated,stars) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._insertSql
        return self._insertSql

    #insert_item 是一个可调用的函数
    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handleError,item,spider)

    #真正进行插入数据库时进行调用
    def insert_item(self,cursor,item):
        try:
            cursor.execute(self.insertSql,(item["articleid"],item["url"],item["content"],item["title"],
                                                item["author"], item["publicdate"], item["text_num"], item["read_num"],
                                                item["comment_num"], item["like_num"], item["cated"], item["stars"]))

        except Exception as e:
            print("e============"+str(e.args))

    #如果发生了数据库的插入错误就会调用这个函数
    def handleError(self,error,item,spider):
        print(error)
