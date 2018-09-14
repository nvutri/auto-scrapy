# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy

from scrapy.loader.processors import Join, Compose, MapCompose, TakeFirst
from w3lib.html import remove_tags


def strip_non_unicode(value):
    """Strip non unicode characters."""
    UNICODE_PATTERN = r'[^\x00-\x7F]+'
    try:
        value = re.sub(UNICODE_PATTERN, '', value)
        return value.strip()
    except Exception:
        return value


def clean_price(value):
    value = value.replace('$', '')
    return float(value)


class JoinStripped(Join):
    """Join a stripped list of strings."""

    def __call__(self, values, separator=', '):
        stripped_text = [strip_non_unicode(t) for t in values if t.strip()]
        single_string = separator.join(stripped_text)
        return single_string.strip()


class StrippedField(scrapy.Field):
    """Input_processor and output_processor are default to be stripping."""

    def __init__(self, *args, **kwargs):
        if 'input_processor' not in kwargs:
            kwargs['input_processor'] = MapCompose(remove_tags)
        if 'output_processor' not in kwargs:
            kwargs['output_processor'] = JoinStripped()
        super(StrippedField, self).__init__(*args, **kwargs)


class PriceField(scrapy.Field):
    def __init__(self, *args, **kwargs):
        kwargs['input_processor'] = MapCompose(remove_tags, clean_price)
        kwargs['output_processor'] = TakeFirst()
        super(PriceField, self).__init__(*args, **kwargs)


class JoinUnique(Join):
    """Join a stripped list of strings."""

    def __call__(self, values, separator=', '):
        stripped_text = [strip_non_unicode(t) for t in values if t.strip()]
        uniq_list = []
        for elem in stripped_text:
            if elem not in uniq_list:
                uniq_list.append(elem)
        single_string = separator.join(uniq_list)
        return single_string.strip()


class FashionItem(scrapy.Item):
    """Item for fashion website."""
    photos = StrippedField(output_processor=JoinUnique())
    record_id = scrapy.Field(output_processor=TakeFirst())
    material = StrippedField()
    fit = StrippedField()
    title = StrippedField()
    price = PriceField()
    sizes = StrippedField(output_processor=JoinUnique())
    colors = StrippedField()
    link = StrippedField()
    details = StrippedField()
    brand_title = StrippedField()
    brand = StrippedField()
