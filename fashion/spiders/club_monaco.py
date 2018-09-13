import json
import re
import scrapy
import requests

from datetime import datetime
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy import log

from fashion.items import FashionItem


class ClubMonacoSpider(CrawlSpider):
    name = "club_monaco"
    start_urls = 'http://www.clubmonaco.com/home/index.jsp'

    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="flyout-header-menu"]//ul/li/a'),
            callback='parse_start_url',
            follow=True
        ),
    ]

    def __init__(self, *args, **kwargs):
        super(ClubMonacoSpider, self).__init__(*args, **kwargs)

    def parse_start_url(self, response):
        """Initial parse for start_urls. """
        results = []
        self.scraped_links.add(response.url)
        for listing in response.xpath('//ol[@id="products"]/li'):
            loader = ItemLoader(item=FashionItem(), selector=listing)
            loader.add_xpath('record_id', '@id')
            # loader.add_xpath('material', '//div[@class="product-details"]')
            # loader.add_xpath('fit', '')
            loader.add_xpath('title', '//div[@class="product-details"]/h6/text()')
            loader.add_xpath('price', '//div[@class="product-details"]/a/span/text()')
            # loader.add_xpath('sizes', '')
            loader.add_xpath('photo', '//div[@class="product-photo"]/a/img/@src')
            loader.add_xpath('colors', '//div[@class="colors"]/ul/li/a/@title')
            loader.add_xpath('link', '//div[@class="product-details"]/h6/a/@href')
            # loader.add_xpath('details', '')
            # loader.add_xpath('brand_title', '')
            # loader.add_xpath('brand', '')
            results.append(loader.load_item())
        return results
