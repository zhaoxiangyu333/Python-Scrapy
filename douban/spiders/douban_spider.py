# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称
    name = 'douban_spider'
    # 允许爬的域名
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['http://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath("//*[@id='content']/div/div[1]/ol/li")
        for movie in movie_list:
            # 导入items.py文件
            douban_item = DoubanItem();
            douban_item['serial_numbber'] = movie.xpath('.//div/div[1]/em/text()').extract_first()
            douban_item['movie_name'] = movie.xpath('.//div/div[2]/div[1]/a/span/text()').extract_first()
            introduceLines = movie.xpath('.//div/div[2]/div[2]/p[1]/text()').extract()
            for line in introduceLines:
                line_introducelines = "".join(line.split())
                douban_item['movie_introduce'] = line_introducelines

            douban_item['movie_star'] = movie.xpath('.//div/div[2]/div[2]/div/span[2]/text()').extract_first()
            douban_item['movie_evaluate'] = movie.xpath('.//div/div[2]/div[2]/div/span[4]/text()').extract_first()
            douban_item['movie_describe'] = movie.xpath('.//div/div[2]/div[2]/p[2]/span/text()').extract_first()
            # 将数据yield到pipelines中
            yield douban_item

        # 下一页的解析
        next_link = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250'+next_link,callback=self.parse)
