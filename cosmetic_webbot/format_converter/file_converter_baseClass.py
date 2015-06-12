# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:01:29 2015

@author: Taikor
"""


import xlrd
import xlsxwriter
from lib import retrive_basename, retrive_dirname


class converter:
    
    EXCEL = 'excel'
    TXT = 'txt'
    CSV = 'csv'
    # define Marcos here
    
    def __init__(self, file_path, from_, to_):
        self.file_path = file_path
        self.from_ = str.lower(from_)
        self.to_ = str.lower(to_)
        
    def xls_to_TABtxt_converter(self):
        workbook = xlrd.open_workbook(self.file_path)
        sheet = workbook.sheet_by_index(0)    # retrive the very first sheet in excel file
        nrows = sheet.nrows
        ncols = sheet.ncols

        lines = list()        
        for row in range(nrows):
            line = ""
            for col in range(ncols):
                line = line + str(sheet.cell_value(row, col)) + "\t"
            line = line[:-1]   # remove the a special character: \t
            line = line + '\n' # add the a special character: \n
            lines.append(line)
        str_lines = "".join(lines)
        
        filted_basename = retrive_basename(self.file_path).replace('xlsx', 'txt')
        filted_dirname = retrive_dirname(self.file_path)
        if len(filted_dirname) > 0:
            f_path = filted_dirname + '\\' + filted_basename
        else:
            f_path = filted_basename
            
        with open(f_path, 'w') as f:
            f.write(str_lines)
            
        return f_path

    def TABtxt_to_xls_converter(self):
        filted_basename = retrive_basename(self.file_path).replace('txt', 'xlsx')
        filted_dirname = retrive_dirname(self.file_path)
        if len(filted_dirname) > 0:
            f_path = filted_dirname + '\\' + filted_basename
        else:
            f_path = filted_basename
        
        workbook = xlsxwriter.Workbook(f_path)  # create a new xlsx file
        worksheet = workbook.add_worksheet()
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
          
        row = 0
        for line in lines:
            line = line.decode("utf-8")
            str_list = line.split('\t')
            col = 0
            for cell_value in str_list:
                worksheet.write(row, col, cell_value)
                col += 1
            row += 1
        workbook.close()
        
        return f_path
                      
    def __call__(self):
        if (self.from_ == converter.EXCEL) and (self.to_ == converter.TXT):
            return self.xls_to_TABtxt_converter()
       
        elif (self.from_ == converter.TXT) and (self.to_ == converter.EXCEL):
            return self.TABtxt_to_xls_converter()
        
