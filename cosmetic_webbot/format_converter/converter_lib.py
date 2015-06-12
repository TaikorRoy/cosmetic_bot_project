# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import os
import json
from file_converter_baseClass import converter


def json_to_txt(file):
    with open(file, 'r') as f:
        content = f.read()

    lines = list()
    keys = ("sku_name", "B2C_platform", "price", "vendor_url", "source_name", "scrapping_time", "sales_volume", "comments")

    products = json.loads(content)

    for product in products:
        buffer = list()
        test_key_existance = True
        for key in keys:
            if key not in product:
                test_key_existance = False
        if test_key_existance:
            for key in keys:
                buffer.append(product[key])
        line = '\t'.join(buffer)
        lines.append(line)
    s = '\n'.join(lines)

    with open(file+'.txt', 'w') as f:
        f.write(s.encode('utf-8'))

    return(file+'.txt')


def txt_to_excel(file):
    excel_to_txt_con = converter(file, "Txt", "Excel")
    new_path = excel_to_txt_con()
