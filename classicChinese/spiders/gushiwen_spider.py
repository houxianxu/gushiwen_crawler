# -*- coding: utf-8 -*-

import scrapy
import re
from classicChinese.items import ClassicchineseItem

N = 5000  # number of pages


def skip_bracket(string):
    """ Skip the bracket and the content in it
        Chinese and English brackets
    """
    # string = string.encode('utf8')
    string = re.sub(r'（.*?）', '', string)
    string = re.sub(r'\(.*?\)', '', string)
    string = re.sub(r'\(.*?）', '', string)
    string = re.sub(r'（.*?\)', '', string)
    return string


class DmozSpider(scrapy.Spider):
    name = "gushiwen"
    allowed_domains = ["gushiwen.org"]
    # start_urls = ["http://so.gushiwen.org/guwen/bfanyi_{}.aspx".format(i) for i in xrange(1, N + 1)]
    start_urls = ["http://so.gushiwen.org/fanyi_{}.aspx".format(i) for i in xrange(1, N + 1)]
    # start_urls = ["http://so.gushiwen.org/fanyi_4903.aspx"]

    def parse(self, response):
        # process response, replace <br /> to '\n'
        response = response.replace(body=response.body.replace('<br>', '\n')) 
        response = response.replace(body=skip_bracket(response.body))
        
        item = ClassicchineseItem()
        item['original'] = None
        item['translated'] = None
        item['title'] = None
        item['url_id'] = response.url.strip().split('/')[-1].split('.')[0]

        # get the title
        title_list = response.xpath('//div[@class="sontitle"]/span/a/text()').extract()
        title_str = ''.join(title_list).strip()
        item['title'] = title_str

        # crawl translated part
        
        translated_str = ''
        
        # before extract from paragraphs, it is needed to check whether there is any text in <div>
        # e.g.http://so.gushiwen.org/guwen/bfanyi_764.aspx
        div_text_list = response.xpath('//div[@class="shileft"]//div[@class="shangxicont"]/text()').extract()
        div_text_str = '\n'.join(x.strip() for x in div_text_list)  # preserve the \n
        div_text_str = div_text_str.strip()  # maybe there are ['\n\n'] in the list
        if div_text_str != '': div_text_str += '\n'
        translated_str += div_text_str

        # scrapt from paragraphs
        trans_paras = response.xpath('//div[@class="shileft"]//div[@class="shangxicont"]//p')

        i = 0
        for p in trans_paras:
            if i == 0:  # skip '作者: 佚名'
                i += 1
                continue
            p_text_list = p.xpath('.//text()').extract()
            p_text_str = ''.join(p_text_list).strip() + '\n'
            # p_text_str = skip_bracket(p_text_str) + '\n'
            if p_text_str[:2] == '注释'.decode('utf8'):  # skip the explanation
                break
            if p_text_str == '参考资料：\n'.decode('utf8'): # skip this paragraph
                continue
            i += 1
            translated_str += p_text_str
        item['translated'] = translated_str
        item['n_trans'] = len(translated_str.strip().split('\n'))


        # crawl original part
        orig_str = ''

        # before extract from paragraphs, it is needed to check whether there is any text in <div>
        # e.g.http://so.gushiwen.org/guwen/bfanyi_50.aspx
        div_text_list = response.xpath('//div[@class="shisoncont"]//text()').extract()  # should be //text e.g.fanyi_4093
        div_text_str = '\n'.join(x.strip() for x in div_text_list)
        div_text_str = div_text_str.strip()

        if div_text_str != '': div_text_str += '\n'
        orig_str += div_text_str
        orig_paras = response.xpath('//div[@class="shisoncont"]//p')
        for p in orig_paras:
            p_text_list = p.xpath('.//text()').extract()
            p_text_str = ''.join(p_text_list).strip() + '\n'
            # p_text_str = skip_bracket(p_text_str).strip() + '\n'
            if p_text_str == '\n': continue
            orig_str += p_text_str
        item['original'] = orig_str
        item['n_ori'] = len(orig_str.strip().split('\n'))

        yield item