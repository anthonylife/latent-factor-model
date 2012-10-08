#!/usr/bin/env python
#encoding=utf8

## This script randomly sample negative instance for training.

import sys
import random

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <user_group_all.in> <ins.in> <pos_ins.in> <neg_pos_ratio.in> <neg_ins.out>'
        sys.exit(1)

    user_groups = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if user_groups.has_key(res[0]):
            user_groups[res[0]].add(res[1])
        else:
            user_groups[res[0]] = set([res[1]])

    groups_set = set([])
    for line in open(sys.argv[2]):
        res = line.strip('\n')
        groups_set.ad(res)

    sample_ratio = int(sys.argv[4])

    wfd = open(sys.argv[5], 'w')
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')[0]
        samples = random.sample(groups_set - user_groups[res], sample_ratio)
        for sample in samples:
            wfd.write('%s,%s\n' % (res, sample))
    wfd.close()
