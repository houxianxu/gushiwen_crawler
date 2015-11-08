# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ClassicchineseItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # title of the article
    original = scrapy.Field()  # original article
    n_ori = scrapy.Field()  # number of paragraphs of original article
    translated = scrapy.Field()  # translated article
    n_trans = scrapy.Field()  # number of paragraphs of translated article
    url_id = scrapy.Field()  # url id scrapt from


