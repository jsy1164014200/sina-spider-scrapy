# -*- coding: utf-8 -*-
import scrapy


class SinanewsItem(scrapy.Item):
    path_name = scrapy.Field()
    title = scrapy.Field()
    # 新闻的内容
    content = scrapy.Field() 
    # url = scrapy.Field()