# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
from scrapy.exceptions import DropItem
import csv

class YahooStockNewsPipeline(object):
    exclude = ["【公告】", "《證交所》"] # 建立需要排除的關鍵字清單

    def open_spider(self, spider):
        self.file = open('stock_news.json', 'a')

    def process_item(self, item, spider):
        title = item['title']
        with open("stock_news.json", "r") as f:
            for line in f.readlines():
                data = json.loads(line)
                if title  in data['title']:
                    raise DropItem('發現重複標題 %s', item)
        if YahooStockNewsPipeline.containsKeyword(title):
            raise DropItem('沒有用的新聞 %s', item)
        else:
            content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(content)
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
