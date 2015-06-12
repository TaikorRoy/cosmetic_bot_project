# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import json
import codecs
import os


def load_product_obj(myfile):
    with codecs.open(myfile, 'r', encoding='utf-8') as f:
        s = f.read()
    json_obj = json.loads(s)
    return json_obj

if __name__ == "__main__":
    base_path = r'C:\workspace\WebCrawler\scrapy_workspace2\jd_search'
    relative_path = r'tutorial\data\catalog\JingHua.json'
    real_path = os.path.join(base_path, relative_path)
    products = load_product_obj(real_path)

