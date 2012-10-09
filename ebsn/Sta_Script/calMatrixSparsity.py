#!/usr/bin/env python
#encoding=utf8
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'usage: <sparse_matrix.in>'
        sys.exit(1)

    user = set()
    group = set()
    entity_cnt = 0
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if res[0] not in user:
            user.add(res[0])
        if res[1] not in group:
            group.add(res[1])
        entity_cnt += 1

    total_cnt = len(user) * len(group)
    print 'Matrix sparsity: %f' % (entity_cnt*1.0/total_cnt)
