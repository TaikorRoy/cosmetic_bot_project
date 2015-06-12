# -*- coding: utf-8 -*-

import os
import sys
import re
import json
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


def strip_quotations(str_a):
    str_a = str_a.replace("\'", "")
    str_a = str_a.replace("\"", "")
    return str_a


class TaoBaoSpider(scrapy.Spider):
    name = "TaoBao"
    allowed_domains = [""]
    start_urls = ("http://s.taobao.com/search?q="+kw+"&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=1.7274553.1997520841.1&initiative_id=tbindexz_20150609" for kw in kw_list)

    def parse(self, response):
        return_test = False  # return number test is omitted
        description_test = False

        # might have a problem regarding 'if not match' statement
        description_match = re.search(u"抱歉！没有找到与", response.body)
        if not description_match:
            description_test = True

        if description_test:
            body = response.body
            match = re.search(r'("itemlist".+?),"shopcombo"', body)
            if match:
                taobao_json_str = match.group(1)
                taobao_json_str = taobao_json_str.lstrip(r'"itemlist": ')  # create a valid string for json obj
                item_json = json.loads(taobao_json_str)
                if "data" in item_json:
                    if "auctions" in item_json["data"]:
                        item_list = item_json["data"]["auctions"]

                        for it in item_list:
                            item = TutorialItem()
                            # vendor_url(unicode)
                            if "detail_url" in it:
                                buffer_vendor_url = strip_quotations(it["detail_url"])
                                item["vendor_url"] = buffer_vendor_url

                            # source_name(unicode)
                            if "raw_title" in it:
                                buffer_source_name = strip_quotations(it["raw_title"])
                                item["source_name"] = buffer_source_name

                            # price(float)
                            if "view_price" in it:
                                buffer_price = float(it["view_price"])
                                item["price"] = buffer_price

                            # scrapping_time(float)
                            item["scrapping_time"] = time.time()

                            # sales_volume(int)
                            if "view_sales" in it:
                                buffer_sales_volume = int(it["view_sales"][:-3])
                                item["sales_volume"] = buffer_sales_volume

                            # comments(int)
                            item["comments"] = -999

                            # sku_name(str)
                            unicode_response_url = urllib.unquote(response.url)
                            match = re.search(r"q=(.+)&commend", unicode_response_url)
                            if match:
                                buffer_sku_name = match.group(1)  # retrive the first subpattern
                            else:
                                buffer_sku_name = "NA"
                            buffer_sku_name = html_stripper2(buffer_sku_name)
                            buffer_sku_name = html_stripper1(buffer_sku_name)
                            buffer_sku_name = strip_quotations(buffer_sku_name)
                            item['sku_name'] = buffer_sku_name

                            # B2C_platform(int)
                            item['B2C_platform'] = 2

                            yield item