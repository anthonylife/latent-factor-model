#!/usr/bin/env python
#encoding=utf8

import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'usage: <freq.in> <prob.out>'
        sys.exit(1)

    totalCnt = 0
    for line in open(sys.argv[1]):
        totalCnt += int(line.strip('\n').split(',')[1])

    cumprob = 0
    wfd = open(sys.argv[2], 'w')
    for line in open(sys.argv[1]):
        [dis, cnt]= line.strip('\n').split(',')
        prob = int(cnt)*1.0/totalCnt
        cumprob += prob
        wfd.write(str(dis)+','+str(cnt)+','+str(prob)+','+str(cumprob)+'\n')
    wfd.close()
