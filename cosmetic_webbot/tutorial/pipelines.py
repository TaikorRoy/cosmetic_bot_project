# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import logging
import logging.handlers

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from tutorial import settings
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


LOG_FILE = 'pipeline.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('pipeline')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



class LocalFilePipeline(object):
    B2C_platform = ["JingDong", "TaoBao", "Jumei"]

    def __init__(self):
        self.file = {site: codecs.open(site, 'wb', encoding='utf-8') for site in LocalFilePipeline.B2C_platform}
        # create empty files named as the file names listed in the relative_path
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        if len(item.keys()) == 8:
            line = json.dumps(dict(item))
            line = line.replace('}', '},')
            line += '\n'
            self.file[spider.name].write(line.decode("unicode_escape"))
            # write data into a file, the name of the file is given by the name attribute of spider object (spider.name)
        return item

    def spider_closed(self, spider):
        logger.debug(spider.name+"Closed")     # bug here, only jingdong spider closed signal was triggered
        self.file[spider.name].close()
        # close the file: spider.name
        with open(spider.name, 'r') as f:
            s = f.read()
            s = s.rstrip(',\n')
            s = '[' + s + ']'
        with open(spider.name, 'w') as f:
            f.write(s)


class MySQLdbPipelineSyn(object):
    """ Synchronous Db connection """
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        logger.debug("MySQLdbPipelineSyn Created.")
        self.db = MySQLdb.Connect(
            host=settings.MySQLdb_SERVER,
            user=settings.MySQLdb_USER,
            passwd=settings.MySQLdb_PASSWD,
            db=settings.MySQLdb_DB,
        )
        self.db.query('SET NAMES %s' % settings.MySQLdb_CHARSET)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if len(item.keys()) == 8:
            if type(item["source_name"]) == str:
                item["source_name"] = unicode(item["source_name"], encoding='utf8')
            if type(item["sku_name"]) == str:
                item["sku_name"] = unicode(item["sku_name"], encoding='utf8')
            if type(item["vendor_url"]) == str:
                item["vendor_url"] = unicode(item["vendor_url"], encoding='utf8')
            sql = r"INSERT INTO skuprice (vendor_url, source_name, price, scrapping_time, sales_volume, comments, sku_name, B2C_platform) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item["vendor_url"], item["source_name"], item["price"], item["scrapping_time"], item["sales_volume"], item["comments"], item["sku_name"], item["B2C_platform"])
            # variable sql is a unicode string
            sql = sql.encode('utf8')   # convert sql to a str type object

            # logger.debug(sql)

            self.cursor.execute(sql)
            self.db.commit()
            return item

    def spider_closed(self, spider):
        self.db.close()
        logger.debug(spider.name+" Spider Closed.")   # logger.debug method never triggered, reason unknown

    # Maybe we should add an pipeline closing method here to clean up in addition to the spider_closed method,
        # but "pipeline_closed" method can be never found in any documentation, maybe this method is not exist


class MySQLdbPipelineAsyn(object):
    """ Asynchronous Db Connection """
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            host=settings.MySQLdb_SERVER,
            user=settings.MySQLdb_USER,
            passwd=settings.MySQLdb_PASSWD,
            db=settings.MySQLdb_DB,
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf-8',
            use_unicode=False
        )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        if len(item.keys()) == 8:
            sql = "INSERT INTO skuprice (vendor_url) VALUES (%s)"
            tx.execute(sql, (item["vendor_url"],))