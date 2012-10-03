#!/usr/bin/env python
#encoding=utf8

# This function calculate the number of groups which holds at least one event the distance of which is within a specified value from users
'''
python getNumUG.py ../Meetup_geo/user_lon_lat.csv ../Meetup_geo/event_lon_lat.csv ../Temporal_Data/user_near_event.csv
python getNumUG.py ../Temporal_Data/user_near_event.csv ../Meetup_network/user_group.csv ../Temporal_Data/user_near_group.csv
'''
import sys
import datetime
from math import ceil
from random import shuffle
from geopy import distance

dis_threshold = 10
user_samples = 200

def getNumEUD(user_location_file, event_location_file, user_near_event_file):
    user_location_dic = {}
    for line in open(user_location_file):
        res =line.strip('\n').split(',')
        user_location_dic[res[0]] = res[1:]
    user_location_dic = user_location_dic.items()
    shuffle(user_location_dic)      # Random shuffle and get
    user_location_dic = dict(user_location_dic[:user_samples])

    wfd = open(user_near_event_file, 'w')
    index = 0
    begin = datetime.datetime.now()
    for line in open(event_location_file):
        index += 1
        if index % 10000 == 0:
            print 'Finish %d ......' % index
            end = datetime.datetime.now()
            print 'Cost time:%d' % (end-begin).seconds
            begin = datetime.datetime.now()
        res = line.strip('\n').split(',')
        for user in user_location_dic.keys():
            if distance.distance(user_location_dic[user], res[1:]).miles < dis_threshold:
                wfd.write('%s,%s\n' % (user, res[0]))
    wfd.close()

def getNumUGD(user_near_event_file, event_group_file, user_near_group_file):
    user_group = {}
    event_user = {}
    for line in open(user_near_event_file):
        res = line.strip('\n').split(',')
        if event_user.has_key(res[1]):
            event_user[res[1]] += res[0:1]
        else:
            event_user[res[1]] = res[0:1]

    for line in open(event_group_file):
        res = line.strip('\n').split(',')
        if event_user.has_key(res[0]):
            for user in event_user[res[0]]:
                if user_group.has_key(user):
                    user_group[user] += res[1:]
                else:
                    user_group[user] = res[1:]

    cnt_group = 0
    max_cnt = 1000
    min_cnt = 1000
    wfd = open(sys.argv[3], 'w')
    for user in user_group.keys():
        temp_cnt = len(user_group[user])
        wfd.write('%s,%d\n' % (user, temp_cnt))
        if temp_cnt > max_cnt:
            max_cnt = temp_cnt
        elif temp_cnt < min_cnt:
            min_cnt = temp_cnt
        cnt_group += temp_cnt
    wfd.close()
    print 'User average group:'
    print 'Max group num: %d...' % max_cnt
    print 'Min group num: %d...' % min_cnt
    print 'Average group num: %f...' % ceil(cnt_group*1.0/user_samples)

if __name__ == "__main__":
    '''if len(sys.argv) != 4:
        print 'usage: <user_location.in> <event_location.in> <user_near_event.out>'
        sys.exit(1)
    getNumEUD(sys.argv[1], sys.argv[2], sys.argv[3])'''

    if len(sys.argv) != 4:
        print 'usage: <user_near_event.in> <user_group.in> <user_near_group.out>'
        sys.exit(1)
    getNumUGD(sys.argv[1], sys.argv[2], sys.argv[3])
