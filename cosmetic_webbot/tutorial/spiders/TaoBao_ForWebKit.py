# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import urllib
import scrapy

from tutorial.items import TutorialItem
from tutorial.spiders.load_product_obj import load_product_obj

base_path = sys.path[0]
relative_path = r'tutorial\data\catalog'
real_path = os.path.join(base_path, relative_path)
jobs = os.listdir(real_path)
jobs = map(lambda x: os.path.join(real_path, x), jobs)

kw_list = list()
for job in jobs:
    products = load_product_obj(job)
    for product in products:
        kw_list.append(product["title"][0])


def html_stripper1(str_a):
    line = str_a
    patterns = ['' for i in range(4)]
    patterns[0] = r'<atarget.+?>'
    patterns[1] = r'<fontclass.+?>'
    patterns[2] = r'</font>'
    patterns[3] = r'<fontclass.+?</font>'
    for pattern in patterns:
        line = re.sub(pattern, "", line, re.DOTALL)
    return line


def html_stripper2(str_a):
    line = str_a
    patterns = ['' for i in range(4)]
    patterns[0] = '\\r'
    patterns[1] = '\\n'
    patterns[2] = '\\t'
    patterns[3] = ' '
    for pattern in patterns:
        line = re.sub(pattern, "", line, re.DOTALL)
    return line


def tag_stripper(mystr):
    line = mystr
    pattern = r"<.+?>"
    line = re.sub(pattern, "", line, re.DOTALL)
    return line


class TaoBaoSpider(scrapy.Spider):
    name = "TaoBao"
    allowed_domains = [""]
    start_urls = ("http://s.taobao.com/search?q="+kw+"&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=1.7274553.1997520841.1&initiative_id=tbindexz_20150609" for kw in kw_list)

    def parse(self, response):
        return_test = False
        description_test = False

        return_result_str = response.xpath("//span[@class='total']/text()").extract()
        if len(return_result_str) > 0:
            return_match = re.search(r"[0-9]+?", return_result_str[0])
            if return_match:
                return_test = True

        description_match = response.xpath("//ul[@class='clearfix']/li").extract()
        if len(description_match) > 0:     # Test if taobao returns result description
            description_match = tag_stripper(description_match[0])
            description_match = re.search(r"抱歉", description_match)
            if not description_match:
                description_test = True

        if return_test & description_test:
            for sel in response.xpath("//div[@id='mainsrp-itemlist']/div[@class='m-itemlist']/div[@class='grid']/div[@id='J_itemlistCont']/div[@class='item  ']"):
                # if no match for the xpath exist, then this iteration will not even being processed.
                item = TutorialItem()

                # vendor_url(str)          ** item name and item data type
                sel_result = sel.xpath("div[@class='row row-2 title']/a/@href").extract()
                if len(sel_result) > 0:
                    # test if there is valid data scrapped
                    buffer_vendor_url = sel_result[0]
                    item['vendor_url'] = html_stripper2(buffer_vendor_url)

                # source_name(str)
                sel_result = sel.xpath("div[@class='row row-2 title']/a").extract()
                if len(sel_result) > 0:
                    buffer_source_name = sel_result[0]
                    buffer_source_name = html_stripper2(buffer_source_name)
                    item['source_name'] = tag_stripper(buffer_source_name)

                # price(float)
                sel_result = sel.xpath("div[@class='price g_price g_price-highlight']/strong/text()").extract()
                if len(sel_result) > 0:
                    buffer_price = sel_result[0]
                    buffer_price = html_stripper2(buffer_price)
                    buffer_price = float(buffer_price)   # convert to float type
                    item['price'] = buffer_price

                # scrapping_time(float)
                item['scrapping_time'] = time.time()

                # sales_volume(int)
                sel_result = sel.xpath("div[@class='row row-1 g-clearfix']/div[@class='deal-cnt']/text()").extract()
                if len(sel_result) > 0:
                    buffer_sales_volume = sel_result[0]
                    match = re.search(r"[0-9]+?", buffer_sales_volume)
                    buffer_sales_volume = match.group(0)
                    buffer_sales_volume = int(buffer_sales_volume)
                    item['sales_volume'] = buffer_sales_volume
                    # no sales_volume data is available

                # comments(int)
                item['comments'] = -999  # Error Code -999 indicates that no comments data are available

                # sku_name(str)
                unicode_response_url = urllib.unquote(response.url)
                # unicode_response_url = unicode(unicode_response_url)
                match = re.search(r"q=(.+)&commend", unicode_response_url)
                if match:
                    buffer_sku_name = match.group(1)  # retrive the first subpattern
                else:
                    buffer_sku_name = "NA"
                buffer_sku_name = html_stripper2(buffer_sku_name)
                buffer_sku_name = html_stripper1(buffer_sku_name)
                item['sku_name'] = buffer_sku_name

                # B2C_platform(str)
                item['B2C_platform'] = u"淘宝"

                yield item