# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings


class FashionImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        photo_path = super(FashionImagesPipeline, self).file_path(request, response=response, info=info)
        return photo_path.replace('full/', 'test/')

    def item_completed(self, results, item, info):
        image_paths = ['%s/%s' % (settings['SPIDER'], x['path']) for ok, x in results if ok]
        item['photos'] = image_paths
        return item


class FashionPipeline(object):
    def open_spider(self, spider):
        self.file = open('%s.csv' % spider.name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item( item )
        print(item)
        return item
