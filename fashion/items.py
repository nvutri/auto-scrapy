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


class FashionItem(scrapy.Item):
    """Item for fashion website."""
    url = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(output_processor=TakeFirst())
    record_id = scrapy.Field(output_processor=TakeFirst())
    material = StrippedField()
    fit = StrippedField()
    title = StrippedField()
    price = StrippedField()
    sizes = StrippedField()
    photos = StrippedField()
    colors = StrippedField()
    link = StrippedField()
    details = StrippedField()
    brand_title = StrippedField()
    brand = StrippedField()
