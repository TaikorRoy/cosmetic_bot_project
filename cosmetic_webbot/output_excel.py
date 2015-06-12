__author__ = 'Taikor'

from tutorial.pipelines import LocalFilePipeline
from format_converter.converter_lib import json_to_txt
from format_converter.converter_lib import txt_to_excel


def output_excel():
    raw_outputs = LocalFilePipeline.B2C_platform
    for raw_output in raw_outputs:
        txt = json_to_txt(raw_output)
        txt_to_excel(txt)

if __name__ == "__main__":
    output_excel()
