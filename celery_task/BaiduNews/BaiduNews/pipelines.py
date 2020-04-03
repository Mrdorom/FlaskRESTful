import pymysql


class BaidunewsPipeline(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root",
                                  "AliCentOSMysql123456", "FlaskRESTFul")
        self.cursor = self.db.cursor()

    def open_spider(self, spider):
        print("开启爬虫！！！")

    def process_item(self, item, spider):
        print("=============================")
        print(f"结果：{item}")
        # 使用execute()方法执行SQL语句
        self.cursor.execute("SELECT * FROM user")
        # 使用fetall()获取全部数据
        data = self.cursor.fetchall()
        # 打印获取到的数据
        print("-----------", data)
        return item

    def close_spider(self, spider):
        # 关闭游标和数据库的连接
        self.cursor.close()
        # 如果有修改增加数据等需要commit
        # db.commit()
        self.db.close()
        print("结束")
