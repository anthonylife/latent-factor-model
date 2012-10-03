#!/usr/bin/env python
#encoding=utf8

'''
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Temporal_Data/user_event.temp.2 0 ../Clean_data/user_event.csv
python filterByOneItem.py ../Temporal_Data/group.temp.1 ../Temporal_Data/event_group.temp.1 1 ../Clean_data/event_group.csv
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Meetup_geo/user_lon_lat.csv 0 ../Clean_data/user_lon_lat.csv
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Meetup_tag/user_tag.new 0 ../Temporal_Data/user_tag.temp.1
python filterByOneItem.py ../Temporal_Data/group.temp.1 ../Meetup_tag/group_tag.new 0 ../Temporal_Data/group_tag.temp.1
'''

import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <user.dic> <doc.in> <field.id(1,2,...)> <doc.out>'
        sys.exit(1)

    # Load info
    itemDic = {}
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        itemDic[line] = 1

    wfd = open(sys.argv[4], 'w')
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        if itemDic.has_key(res[int(sys.argv[3])]):
            wfd.write(line)
    wfd.close()
