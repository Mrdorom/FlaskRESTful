# -*- coding: utf-8 -*-
import scrapy

from BaiduNews.items import BaidunewsItem


class BaiduspiderSpider(scrapy.Spider):
    name = 'BaiDuSpider'
    allowed_domains = ['news.baidu.com']
    start_urls = ['http://news.baidu.com/']

    def parse(self, response):
        titles = response.xpath("//div[@class='hotnews']/ul/li")
        item = BaidunewsItem()
        for title in titles:
            item["title"] = title.xpath("./strong/a/text()").get()
            if item["title"] == None:
                continue
            item["url"] = title.xpath("./strong/a/@href").get()
            yield item
