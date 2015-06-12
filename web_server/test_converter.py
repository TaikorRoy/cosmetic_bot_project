# -*- coding: utf-8 -*-
__author__ = 'Taikor'
import os
import pickle
import codecs
import sys
import shutil
module_path = sys.path[0]
sys.path.append(module_path)
from format_converter.converter_lib import json_obj_to_excel
"""
with codecs.open("test_converter.pickle", "rb") as f:
    json_obj = pickle.load(f)
"""
"""
xlsx_path = os.path.join(module_path, "query_result.xlsx")   # absolute path in static folder
print(xlsx_path)
xlsx_path = r"C:/workspace/cosmetic_bot_project111/cosmetic_bot_project/web_server/static/query_result.xlsx"
json_obj = [{"a":"我111", "b":2}, {"a":5, "b":9}]

xlsx_path = "query_result.xlsx"   # absolute path in static folder
json_obj_to_excel(json_obj, xlsx_path)
"""
xlsx_path = os.path.join(module_path, r"static\query_result.xlsx")   # absolute path in static folder

shutil.copy(r"query_result.xlsx", xlsx_path)