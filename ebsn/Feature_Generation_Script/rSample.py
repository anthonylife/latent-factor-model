#!/usr/bin/env python
#encoding=utf8

# This script can the input file by line into specified number of parts.

import sys
import random

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <file.in> <samples_num.in> <file.out>'
        sys.exit(1)

    item_set = []
    for line in open(sys.argv[1]):
        item_set.append(line)

    wfd = open(sys.argv[3]+sys.argv[1]+"."+str(i+1), 'w')
    samples = set(random.sample(item_set, cnt))
    item_set = item_set-samples
    for sample in samples:
        wfd.write(sample)
    wfd.close()
