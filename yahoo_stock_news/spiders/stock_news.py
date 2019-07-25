# -*- coding: utf-8 -*-
import scrapy
import csv
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
from yahoo_stock_news.items import YahooStockNewsItem

df = pd.read_csv("stock50.csv", encoding="big5", header=None)


class StockNewsSpider(scrapy.Spider):
    name = 'stock_news'
    allowed_domains = ['tw.stock.yahoo.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {'yahoo_stock_news.pipelines.YahooStockNewsPipeline':300}
    }
    # with open("/Users/kai/Documents/scrapingEnv/tw_stock/tw_stock/spiders/臺灣上市公司代碼表2019-07-19.csv", newline="") as f:
    #     data = csv.reader(f, delimiter="\t")
    data = df[0]
    for d in data:
        for p in range(1, 51):
            start_urls.append("https://tw.stock.yahoo.com/q/h?s=" + str(d) + "&pg=" + str(p))


    def parse(self, response):
        item = YahooStockNewsItem()
        bs = BeautifulSoup(response.text)
        item['company'] = bs.find("div", {"style":"display: inline-block"}).text
        item['code'] = bs.find("div", {"style":"margin-left: 8px; color: #979ba7; display: inline-block"}).text.strip()
        # print(company, code)
        contents = response.xpath("/html[1]/body[1]/center[1]/table[1]/tbody[1]/tr[1]/td[1]/table[2]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr/td[2]")
        # print(contents)
        ref = "https://tw.stock.yahoo.com"
        for content in contents:
            title = content.xpath("./a[1]//@href").extract()
            if title[0] != "/news/":
                end = title[0]
                url = ref + end
                # print(item, url)
                yield scrapy.Request(url=url, meta={"item":item}, callback=self.parse_content, dont_filter=True)


    def parse_content(self, response):
        # with open("stock_news.json", "r") as f:
        #     for line in f.readlines():
        #         data = json.loads(line)
        #         if response.url in data['url']:
        #             print("有重複了，不抓取，你這個白癡！")
        #             pass
        item = response.meta['item']
        item['title'] = response.xpath("//h1[1]/text()").extract()[0]
        text = response.xpath("//td[1]/p//text()").extract()
        item['content'] = "".join(text).strip()
        item['date'] = response.xpath("//td[@class='yui-text-left']/span/text()").extract()[0]
        item['source'] = response.xpath("//td[@class='yui-text-left']/span/text()").extract()[1]
        yield item