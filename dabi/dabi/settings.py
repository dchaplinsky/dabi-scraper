# -*- coding: utf-8 -*-

# Scrapy settings for dabi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dabi'

SPIDER_MODULES = ['dabi.spiders']
NEWSPIDER_MODULE = 'dabi.spiders'

HTTPCACHE_ENABLED = True
USER_AGENT = 'DABI crawler bot (https://github.com/dchaplinsky/dabi-scraper)'
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 1

HTTPCACHE_IGNORE_HTTP_CODES = [403, 404, 500, 503]
HTTPCACHE_POLICY = "dabi.cache.ItemNumbersMetaDummyPolicy"
