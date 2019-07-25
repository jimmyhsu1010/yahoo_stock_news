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
    # def process_item(self, item, spider):
        # now = time.strftime("%Y-%m-%d", time.localtime())
        # filename = "tw_stock_news" + now + ".csv"
        # with open(filename, "a") as f:
        #     f.write("item['date']" + "\t")
        #     f.write("item['code']" + "\t")
        #     f.write("item['company']" + "\t")
        #     f.write("item['source']" + "\t")
        #     f.write("item['title']" + "\t")
        #     f.write("item['content']" + "\n")
        # return item
    def open_spider(self, spider):
        self.file = open('stock_news.json', 'a')




    def process_item(self, item, spider):
        title = item['title']
        with open("stock_news.json", "r") as f:
            for line in f.readlines():
                data = json.loads(line)
                if title in data['title']:
                    raise DropItem('發現重複標題 %s', item)
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # if item['title'] in content:
        #     raise DropItem("此標題'{}'已經出現過了!!".format(item['title']))
        self.file.write(content)
        return item

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
