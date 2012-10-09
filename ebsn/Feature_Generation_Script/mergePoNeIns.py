#!/usr/bin/env python
#encoding=utf8

## Merge the user group positive instance and negative instance(Without features)

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <directory.in> <filter_str.in> <left_part.in> <pos_train.out> <pos_neg_train.out>'
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print '%s not a directory' % (sys.argv[1])
        sys.exit(1)

    files = os.listdir(sys.argv[1])
    filter_str = sys.argv[2].split(',')

    wfd = open(sys.argv[5], 'w')
    wfd1 = open(sys.argv[4], 'w')
    for f in files:
        # positive
        if filter_str[0] in f and sys.argv[3] not in f:
            for line in open(os.path.join(sys.argv[1], f)):
                wfd.write('1,'+line)
                wfd1.write(line)
        # negative
        elif filter_str[1] in f and sys.argv[3] not in f:
            for line in open(os.path.join(sys.argv[1], f)):
                wfd.write('0,'+line)
    wfd.close()
    wfd1.close()
