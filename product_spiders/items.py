# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
import re


class product_spidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def clear(value):

    if value is None:
        value = ""

    if isinstance( value, str ):
        value = value.strip()
        value = value.replace(u'\xa0', u' ')
        value = unicode(value)

    if isinstance( value, unicode ):
        value = value.strip()
        value = value.replace(u'\xa0', u' ')

    return value

def remove_newlines(value):

    if value is None:
        value = ""

    if isinstance( value, str ):
        value = re.sub( r'[\r\n]', " ", value )
        value = re.sub( r'\s+', " ", value )
        value = re.sub( r'^\s+|\s+$', "", value )
        value = unicode(value)

    if isinstance( value, unicode ):
        value = value.replace(u'\xa0', u' ')
        value = re.sub( r'[\r\n]', " ", value )
        value = re.sub( r'\s+', " ", value )
        value = re.sub( r'^\s+|\s+$', "", value )

    return value

class CsiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    ProductLink = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    ImageLink = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    Rarity = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    ProductTitle = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    NearMintQty = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    NearMintPrice = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    PlayedQty = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    PlayedPrice = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )
    SetName = scrapy.Field( input_processor=TakeFirst(), output_processor=MapCompose(clear) )

    pass
