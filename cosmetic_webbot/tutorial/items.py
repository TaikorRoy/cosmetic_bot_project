# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:

    # Scrapped Items
    vendor_url = scrapy.Field()
    source_name = scrapy.Field()
    price = scrapy.Field()
    scrapping_time = scrapy.Field()
    sales_volume = scrapy.Field()
    comments = scrapy.Field()

    # Generated Items
    sku_name = scrapy.Field()
    B2C_platform = scrapy.Field()
