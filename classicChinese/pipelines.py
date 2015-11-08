# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ClassicchinesePipeline(object):

    def process_item(self, item, spider):
        orig_trans_str = '   |   '.join((item['original'], item['translated'], str(item['n_ori']), str(item['n_trans'])))
        
        # write to local file
        filename = item['url_id'] + '.csv'
        with open(filename, 'w') as f:
            f.write(orig_trans_str.encode('utf8'))
        return item
