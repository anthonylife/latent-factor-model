#!/usr/bin/env python
#encoding=utf8

'''
python filterByTwoItem.py ../Temporal_Data/user.temp.1 ../Temporal_Data/group.temp.1 ../Temporal_Data/user_group.temp.1 0 1 ../Clean_Data/user_group.csv
'''

import sys

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print 'usage: <user.dic> <group.dic> <doc.in> <field.id(1,2,...)> <field.id(1,2,...)> <doc.out>'
        sys.exit(1)

    userDic = {}
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        userDic[line] = 1

    groupDic = {}
    for line in open(sys.argv[2]):
        line = line.strip('\n')
        groupDic[line] = 1

    wfd = open(sys.argv[6], 'w')
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        if userDic.has_key(res[int(sys.argv[4])]) and groupDic.has_key(res[int(sys.argv[5])]):
            wfd.write(line)
    wfd.close()

