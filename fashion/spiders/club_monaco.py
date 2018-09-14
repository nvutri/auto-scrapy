import json
import logging
import scrapy
import re
import requests
import selenium
import time

from datetime import datetime
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy import log

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

from fashion.items import FashionItem


class ClubMonacoSpider(CrawlSpider):
    name = "club_monaco"
    start_urls = ['http://www.clubmonaco.com/category/index.jsp?categoryId=12243591&ab=global_men']

    rules = [
        Rule(
            LinkExtractor(restrict_xpaths='//ul[@class="mlp-subLinks"]/li/a'),
            callback='parse_start_url',
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="product-details"]/h6/a'),
            callback='parse_product',
            follow=False
        ),
    ]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Firefox()
        super(ClubMonacoSpider, self).__init__(*args, **kwargs)

    def parse_start_url(self, response):
        """Initial parse for start_urls. """
        results = []
        return results

    def parse_product(self, response):
        loader = ItemLoader(item=FashionItem(), response=response)
        loader.add_xpath('record_id', '@id')
        loader.add_value('brand', 'clubmonaco')
        loader.add_value('brand_title', 'Club Monaco')
        loader.add_xpath('title', '//div[@id="product-information"]/h1')
        sale_price = response.xpath('//div[@id="product-information"]/div[@class="money"]/span[@class="sale-price"]').extract()
        if not sale_price:
            loader.add_xpath('price', '//div[@id="product-information"]/div[@class="money"]/span')
        else:
            loader.add_value('price', sale_price[ 0 ])
        self.driver.get(response.url)
        sizes = []
        try:
            # self.driver.find_element_by_xpath('//img[@id="cart-Overlay-close"]').click()
            self.driver.find_element_by_xpath('//a[@id="fancybox-close"]').click()
        except selenium.common.exceptions.WebDriverException as e:
            print(e)
        try:
            self.driver.find_element_by_xpath('//fieldset[@id="sizeContainer"]/ul').click()
        except selenium.common.exceptions.ElementClickInterceptedException as e:
            print(e)
        for size in self.driver.find_elements_by_xpath('//fieldset[@id="sizeContainer"]/ul/li'):
            sizes.append(size.text)
        photos = []
        for photo_border in self.driver.find_elements_by_xpath('//ul[@id="alternate-images"]/li/div[@class="image-border"]'):
            try:
                photo_border.click()
                time.sleep( 2 )
            except selenium.common.exceptions.ElementClickInterceptedException as e:
                print(e)
            for big_photo in self.driver.find_elements_by_xpath('//div[@class="s7flyoutzoom"]//img'):
                if big_photo.get_attribute('src'):
                    photos.append(big_photo.get_attribute('src'))
        loader.add_value('sizes', sizes)
        loader.add_value('photo_urls', photos)
        loader.add_xpath('colors', '//fieldset[@id="colorContainer"]/ul[@class="swatches"]/li[@class="swatch"]/text()')
        loader.add_value('link', response.url)
        details_p = response.xpath('//div[@id="tab-details"]/p/text()').extract()
        details_list = response.xpath('//div[@id="tab-details"]/ul/li/text()').extract()
        loader.add_value('details', '. '.join(details_p + details_list ))
        return loader.load_item()
