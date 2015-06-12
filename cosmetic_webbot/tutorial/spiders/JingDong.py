# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import urllib
import scrapy

from tutorial.items import TutorialItem
from tutorial.spiders.load_product_obj import load_product_obj

from tutorial.settings import JingDong_Query_Section_A
from tutorial.settings import JingDong_Query_Section_B

from tutorial.settings import JD_Response_Xpath
from tutorial.settings import JD_Vendor_Url_Xpath
from tutorial.settings import JD_Source_Name_Xpath
from tutorial.settings import JD_Price_Xpath
from tutorial.settings import JD_Comments_Xpath


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
    patterns = ['' for i in range(5)]
    patterns[0] = r'<atarget.+?>'
    patterns[1] = r'<fontclass.+?>'
    patterns[2] = r'</font>'
    patterns[3] = r'<fontclass.+?</font>'
    patterns[4] = r'</a>'
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


def html_stripper3(str_a):
    line = str_a
    patterns = ['' for i in range(4)]
    patterns[0] = '\\r'
    patterns[1] = '\\n'
    patterns[2] = '\\t'
    patterns[3] = ' '
    for pattern in patterns:
        line = line.replace(pattern, "")
    return line


def strip_quotations(str_a):
    str_a = str_a.replace("\'", "")
    str_a = str_a.replace("\"", "")
    return str_a


class JingDongSpider(scrapy.Spider):
    name = "JingDong"
    allowed_domains = [""]
    start_urls = (JingDong_Query_Section_A + kw + JingDong_Query_Section_B for kw in kw_list)

    def parse(self, response):
        for sel in response.xpath(JD_Response_Xpath):
            # if no match for the xpath exist, then this iteration will not even being processed.
            item = TutorialItem()

            # vendor_url(str)          ** item name and item data type
            sel_result = sel.xpath(JD_Vendor_Url_Xpath).extract()
            if len(sel_result) > 0:
                # test if there is valid data scrapped
                buffer_vendor_url = sel_result[0]
                buffer_vendor_url = strip_quotations(buffer_vendor_url)
                buffer_vendor_url = html_stripper2(buffer_vendor_url)
                item['vendor_url'] = html_stripper3(buffer_vendor_url)

            # source_name(str)
            sel_result = sel.xpath(JD_Source_Name_Xpath).extract()
            if len(sel_result) > 0:
                buffer_source_name = sel_result[0]
                buffer_source_name = strip_quotations(buffer_source_name)
                buffer_source_name = html_stripper2(buffer_source_name)
                buffer_source_name = html_stripper3(buffer_source_name)
                item['source_name'] = html_stripper1(buffer_source_name)

            # price(float)
            sel_result = sel.xpath(JD_Price_Xpath).extract()
            if len(sel_result) > 0:
                buffer_price = sel_result[0]
                buffer_price = html_stripper2(buffer_price)
                buffer_price = buffer_price[1:]  # strip the currency notation sign
                buffer_price = float(buffer_price)   # convert to float type
                item['price'] = buffer_price

            # scrapping_time(float)
            item['scrapping_time'] = time.time()

            # sales_volume(int)
            buffer_sales_volume = -999  # Error Code -999 indicates that no sales_volume data are available
            buffer_sales_volume = int(buffer_sales_volume)
            item['sales_volume'] = buffer_sales_volume

            # comments(int)
            sel_result = sel.xpath(JD_Comments_Xpath).extract()
            if len(sel_result) > 0:
                buffer_comments = sel_result[0]
                buffer_comments = html_stripper2(buffer_comments)
                match = re.search(r"[0-9]+", buffer_comments)
                if match:
                    buffer_comments = match.group(0)
                else:
                    buffer_comments = -1  # Error Code -1 indicates
                    # that no comment number can be found, webpage source changed
                buffer_comments = int(buffer_comments)  # convert to float type
                item['comments'] = buffer_comments

            # sku_name(str)
            unicode_response_url = urllib.unquote(response.url)
            # unicode_response_url = unicode(unicode_response_url)
            match = re.search(r"keyword=(.+)&enc", unicode_response_url)
            if match:
                buffer_sku_name = match.group(1)  # retrive the first subpattern
            else:
                buffer_sku_name = "NA"
            buffer_sku_name = html_stripper2(buffer_sku_name)
            buffer_sku_name = html_stripper1(buffer_sku_name)
            buffer_sku_name = strip_quotations(buffer_sku_name)
            item['sku_name'] = buffer_sku_name

            # B2C_platform(int)
            item['B2C_platform'] = 1      # Code 1 represent '京东' in the backend database

            yield item