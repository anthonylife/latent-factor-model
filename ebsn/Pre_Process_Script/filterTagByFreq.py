#!/usr/bin/env python
#encoding=utf8

## This script filters the tag by their frequency.

'''
python filterTagByFreq.py ../Temporal_Data/tag.temp.1 ../Temporal_Data/user_tag.temp.1 ../Temporal_Data/group_tag.temp.1 ../Clean_data/user_tag.csv ../Clean_data/group_tag.csv
'''

import sys

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <tag.in> <user_tag.in> <group_tag.in> <user_tag.out> <group_tag.out>'
        sys.exit(1)

    tag_dic = {}
    for line in open(sys.argv[1]):
        tag_dic[line.strip('\n')] = 1

    wfd = open(sys.argv[4], 'w')
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')[1]
        if tag_dic.has_key(res):
            wfd.write(line)
    wfd.close()

    wfd = open(sys.argv[5], 'w')
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')[1]
        if tag_dic.has_key(res):
            wfd.write(line)
    wfd.close()

