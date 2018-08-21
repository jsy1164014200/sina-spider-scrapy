# -*- coding: utf-8 -*-
import scrapy

from sinanews.items import SinanewsItem
import os


class SinaspiderSpider(scrapy.Spider):
    name = 'sinaspider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        # 遍历每一个 selector对象
        for each in response.xpath('//div[@id="tab01"]/div'):
            # 防止最后一条 地方站报错
            if(each.xpath('./h3/a/text()')):
                # 创建父目录
                parent_file_name = "./Data/" + each.xpath('./h3/a/text()')[0].extract()
                if(not os.path.exists(parent_file_name)):
                    os.makedirs(parent_file_name)

                parent_url = each.xpath('./h3/a/@href')[0].extract()
                # 创建子目录
                for every in each.xpath('./ul/li/a'):
                    sub_file_name = parent_file_name + "/" + every.xpath('./text()')[0].extract()
                    if(not os.path.exists(sub_file_name)):
                        os.makedirs(sub_file_name)
                    
                    sub_url = every.xpath('./@href')[0].extract()

                    obj = {
                        'parent_url':parent_url,
                        'path_name':sub_file_name
                    }
                    yield scrapy.Request(url=sub_url, meta={'obj':obj}, callback=self.detail_parse)




    def detail_parse(self,response):
        # 得到详细页的 每一个新闻的 链接
        obj = response.meta['obj']
        for each in response.xpath('//a/@href').extract():
            if(each.startswith(obj['parent_url'])):
                yield scrapy.Request(url=each,meta={'obj':obj},callback=self.resave_parse)

    def resave_parse(self,response):
        if(response.xpath('//h1/text()')):
            obj = response.meta['obj']
            item = SinanewsItem()
            item['path_name'] = obj['path_name']
            item['title'] = response.xpath('//h1/text()')[0].extract()
            item['content'] = response.xpath('//body/text()')[0].extract()
            yield item
        else:
            return


        
