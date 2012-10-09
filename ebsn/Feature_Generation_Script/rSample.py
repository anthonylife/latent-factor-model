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

    # Sample accroding to the specified number
    if sys.argv[2].find('.') == -1:
        sample_cnt = int(sys.argv[2])
    # Sample accroding to the specified ratio
    else:
        ratio = float(sys.argv[2])
        sample_cnt = len(item_set)*ratio

    wfd = open(sys.argv[3], 'w')
    samples = set(random.sample(item_set, sample_cnt))
    item_set = item_set-samples
    for sample in samples:
        wfd.write(sample)
    wfd.close()
