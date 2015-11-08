# -*- coding: utf-8 -*-

import sys
import os
import re

newline = ['。'.decode('utf-8'), '？'.decode('utf-8'), '！'.decode('utf-8')]

# file_list = os.listdir('./fanyi/')

def split_at_token(string):
    print string, '$$$$$'
    output_str = string[:]
    for token in newline:
        temp_list = output_str.split(token)
        if len(temp_list) > 1:
            output_str = '\n'.join([x + token for x in temp_list if len(x.strip()) != 0])
            output_str = output_str[:-1]
    return output_str + string[-1]


def clean_one_file(filename):
    print filename, '------'
    with open(filename, 'r') as f:
        line_str = f.read()

    line_str = re.sub(r'"', '', line_str)
    line_str = re.sub(r'“', '', line_str)
    line_str = re.sub(r'”', '', line_str)
    line_str = re.sub(r'\n', '', line_str)
    line_list = line_str.strip().split('|')

    if len(line_list) == 0:
        with open('empty_file.csv', 'a') as f:
            f.write(filename)
        return

    # preprocessing translated part
    trans = line_list[1].strip().decode('utf-8')
    if trans[:2] != '译文'.decode('utf-8') and trans[:2] != '释义'.decode('utf-8'):
        print filename, 'no translation, skip ...'
        return
    else:
        trans = trans[2:]
    trans_out = split_at_token(trans)

    # preprocessing original part
    if len(line_list[0]) == 0:  # no original part e.g. fangyi_64
        return

    original = line_list[0].strip().decode('utf-8')
    original_out = split_at_token(original)
    original_list = original_out.strip().split('\n')
    trans_list = trans_out.strip().split('\n')

    # print len(original_list), len(trans_list)
    # print original_out
    # print '---------'
    # print trans_out
    if len(original_list) != len(trans_list):
        with open('error_file.csv', 'a') as f:
            f.write(filename + '\n')
        with open('need_human_clean/' + filename.split('/')[-1], 'w') as f:
            output_str = original_out.strip() + '   |   ' + trans_out
            f.write(output_str.encode('utf-8'))
    else:
        output_str = ''
        for t in zip(original_list, trans_list):
            output_str += '    |    '.join(t) + '\n'

        with open('clean_fanyi/' + filename.split('/')[-1], 'w') as f:
            f.write(output_str.encode('utf-8'))

def clean_all_files(dir):
    file_list = os.listdir(dir)
    for filename in file_list:
        clean_one_file(dir + filename)

if __name__ == '__main__':
    if not os.path.exists('clean_fanyi'):
        os.makedirs('clean_fanyi/')
    if not os.path.exists('need_human_clean'):
        os.makedirs('need_human_clean/')

    dir = './fanyi/'
    clean_all_files(dir)

    # filename = './fanyi/fanyi_999.csv'
    # print clean_one_file(filename)


