# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
from .items import MovieItem


def get_info(item: MovieItem) -> tuple:
    title = item.get('title', '')
    rank = item.get('rank', '')
    descript = item.get('descript', '')
    duration = item.get('duration', '')
    comments = item.get('comments', '')
    return (title, rank, descript, duration, comments)


# 需要在settings中配置管道信息
class ExcelPipeline:
    def __init__(self) -> None:
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = '豆瓣Top250电影'
        self.sheet.append(('标题', '评分', '宣传语', '片长', '影片简介'))

    def close_spider(self, spider):
        self.wb.save('豆瓣TOP250电影.xlsx')

    def process_item(self, item, spider):
        self.sheet.append(get_info(item=item))
        # 注意管道中的此处必须返回一个item
        return item


# 需要在settings中配置管道信息
class MysqlPipeline:
    def __init__(self) -> None:
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            port=3306,
            database='douban_movie',
            passwd='940328',
            charset='utf8',
        )
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if self.data:
            self._save_db()
        self.conn.close()

    def process_item(self, item, spider):
        self.data.append(get_info(item))
        # 写入到mysql时，每100行数据插入一次，批处理
        if len(self.data) == 100:
            self._save_db()
        return item

    def _save_db(self):
        sql = 'insert into top_movie (title, rating, descript, duration, comments) values (%s, %s, %s, %s, %s)'
        self.cursor.executemany(sql, self.data)
        self.conn.commit()
        self.data.clear()
