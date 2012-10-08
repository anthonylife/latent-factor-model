#!/usr/bin/env python
#encoding=utf8

# This script can partition the input file by line into specified number of parts.

import sys
import random

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <file.in> <num_parts> <output_directory>'
        sys.exit(1)

    item_set = []
    for line in open(sys.argv[1]):
        item_set.append(line)

    item_cnt = len(item_set)
    parts = len(sys.argv[2])
    partition_cnt = [item_cnt/parts for i in xrange(parts)]
    partition_cnt[parts-1] += item_cnt%parts

    item_set = set(item_set)
    for i, cnt in enumerate(partition_cnt):
        wfd = open(sys.argv[3]+sys.argv[1]+"."+str(i+1), 'w')
        samples = set(random.sample(item_set, cnt))
        item_set = item_set-samples
        for sample in samples:
            wfd.write(sample)
        wfd.close()
