# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def process_item(self, item, spider):
        with open(item['path_name']+'/'+item['title']+'.txt','w') as f:
            f.write(item['content'])
        return item
