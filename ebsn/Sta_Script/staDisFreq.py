#!/usr/bin/env python
#encoding=utf8

import sys
from math import ceil

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'usage: <user_event_dis.in>'
        sys.exit(1)

    freqDis = {}
    for line in open(sys.argv[1]):
        dis = str(ceil(float(line.strip('\n').split(',')[1])))
        if freqDis.has_key(dis):
            freqDis[dis] += 1
        else:
            freqDis[dis] = 1

    freqDis = freqDis.items()
    freqDis = sorted(freqDis, key=lambda x: x[1], reverse=True)

    wfd = open(sys.argv[2], 'w')
    for item in freqDis:
        wfd.write(str(item) + '\n')
    wfd.close()
