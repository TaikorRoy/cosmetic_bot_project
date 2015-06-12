# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'tutorial.pipelines.LocalFilePipeline': 300,
    #'tutorial.pipelines.MySQLdbPipelineSyn': 500
}


#---------------------------------MySQLdb Connection Macro----------------------------------------#
MySQLdb_SERVER = 'localhost'
MySQLdb_USER = 'root'
MySQLdb_PASSWD = ''
MySQLdb_DB = 'sku'
MySQLdb_CHARSET = 'utf8'
#------------------------------------------------------------------------------------------------#




#---------------------------------Query URL Macro-------------------------------------------------#

JingDong_Query_Section_A = 'http://search.jd.com/Search?keyword='
JingDong_Query_Section_B = '&enc=utf-8'
TaoBao_Query_Section_A = 'http://s.taobao.com/search?q='
TaoBao_Query_Section_B = '&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=1.7274553.1997520841.1&initiative_id=tbindexz_20150609'
Jumei_Query_Section_A = ''
Jumei_Query_Section_B = ''

#-------------------------------------------------------------------------------------------------#




#---------------------------------XPATH Macro-----------------------------------------------------#
#JD = JingDong, JM = Jumei

JD_Response_Xpath = "//ul[@class='list-h clearfix']/li/div[@class='lh-wrap']"     # item-list section xpath
JD_Vendor_Url_Xpath = "div[@class='p-name']/a/@href"                              # one component of item xpath
JD_Source_Name_Xpath = "div[@class='p-name']/a"
JD_Price_Xpath = "div[@class='p-price']/strong/text()"
JD_Comments_Xpath = "div[@class='extra']/a/text()"

JM_Response_Xpath = ""
JM_Vendor_Url_Xpath = ""
JM_Source_Name_Xpath = ""
JM_Price_Xpath = ""
JM_Comments_Xpath = ""

#-------------------------------------------------------------------------------------------------#

