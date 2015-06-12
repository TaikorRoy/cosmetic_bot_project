# -*- coding: utf-8 -*-
__author__ = 'Taikor'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from tutorial.spiders.JingDong import JingDongSpider
from tutorial.spiders.TaoBao import TaoBaoSpider
from tutorial.spiders.Jumei import JumeiSpider
from scrapy.utils.project import get_project_settings

spiders = [JingDongSpider]   # load spider classes


def setup_crawler(spider_class):
    obj_spider = spider_class()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(obj_spider)
    crawler.start()

for spider in spiders:
    setup_crawler(spider)
log.start()
reactor.run()  # the script will block here until the spider_closed signal was sent



