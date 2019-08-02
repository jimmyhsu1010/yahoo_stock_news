# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
from scrapy.exceptions import DropItem
import csv
import pymongo


class YahooStockNewsPipeline(object):
    exclude = ["【公告】", "《證交所》", "上市認購(售)權證", "國際匯市", "證交所鉅額交易日"] # 建立需要排除的關鍵字清單

    def open_spider(self, spider):
        self.file = open('stock_news.json', 'a')
        client = pymongo.MongoClient("mongodb://db102stock:db102stock_pwd@10.120.14.28:27017/stock")
        db = client.stock
        self.collection = db.stock_news

    def process_item(self, item, spider):
        title = item['title']
        with open("stock_news.json", "r") as f:
            for line in f.readlines():
                data = json.loads(line)
                if title in data['title']:
                    raise DropItem('發現重複標題 %s', item)
        if YahooStockNewsPipeline.containsKeyword(title):
            raise DropItem('沒有用的新聞 %s', item)
        else:
            content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(content)
            self.collection.insert(dict(item))
            return item
    '''
    建立關鍵字排除的method
    '''
    @classmethod
    def containsKeyword(cls, title):
        for keyword in cls.exclude:
            if keyword in title:
                return True
        return False


    def close_spider(self, spider):
        self.file.close()


class BooksPipeline(object):
    def __init__(self):
        self.f = open("books.csv", "a", newline="")
        self.fieldnames = ["type", "rank", "name", "author"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close(self,spider):
        self.f.close()



