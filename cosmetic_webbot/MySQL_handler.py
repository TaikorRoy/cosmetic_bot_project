# -*- coding: utf-8 -*-
__author__ = 'Taikor'

import MySQLdb
import codecs
import time
from tutorial import settings

# Standalone MySQL handler,  for debugging use


def MySQL_handler():
    with codecs.open(r"sql_buffer", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            db = MySQLdb.Connect(
                host=settings.MySQLdb_SERVER,
                user=settings.MySQLdb_USER,
                passwd=settings.MySQLdb_PASSWD,
                db=settings.MySQLdb_DB,
            )
            db.query('SET NAMES %s' % settings.MySQLdb_CHARSET)
            cursor = db.cursor()
            sql = line.encode('utf8')
            cursor.execute(sql)
            db.commit()
            db.close()
            time.sleep(0.5)
