#!/usr/bin/env python
#encoding=utf8

'''
python getTagFreq.py ../Temporal_Data/user_tag.temp.1 ../Temporal_Data/group_tag.temp.1 ../Sta_Data/tag_freq.sta ../Temporal_Data/tag.temp.1
'''

import sys

# Threshold of tag frequency
freq_threshold = 10

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <user_tag.in> <group_tag.in> <tag_freq_sta.out> <tag.out>'
        sys.exit(1)

    tag_freq = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if tag_freq.has_key(res[1]):
            tag_freq[res[1]] += 1
        else:
            tag_freq[res[1]] = 1

    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        if tag_freq.has_key(res[1]):
            tag_freq[res[1]] += 1
        else:
            tag_freq[res[1]] = 1

    tag_freq = sorted(tag_freq.items(), key=lambda x: x[1])
    wfd_freq = open(sys.argv[3], 'w')
    wfd_tag = open(sys.argv[4], 'w')
    for tag in tag_freq:
        wfd_freq.write(tag[0] + ',' + str(tag[1]) + '\n')
        if tag[1] > freq_threshold:
            wfd_tag.write(tag[0]+'\n')
    wfd_freq.close()
    wfd_tag.close()
