#!/usr/bin/env python
#encoding=utf8

import sys
from geopy import distance

def checkEventGroup():
    '''Function:
        Check whether a user must join group to attend its events
    '''
    event_group_file = '../Meetup_network/event_group.csv'
    user_group_file = '../Meetup_network/user_group.csv'
    user_event_file = '../Meetup_network/user_event.csv'

    event_group = {}
    for line in open(event_group_file):
        line = line.strip('\n')
        res = line.split(',')
        if event_group.has_key(res[0]):
            print 'Error in event key.'
            sys.exit(1)
        event_group[res[0]] = res[1]

    user_group = {}
    for line in open(user_group_file):
        line = line.strip('\n')
        res = line.split(',')
        if user_group.has_key(res[0]):
            user_group[res[0]] += [res[1]]
        else:
            user_group[res[0]] = [res[1]]

    inCount = 0
    outCount = 0
    for line in open(user_event_file):
        line = line.strip('\n')
        res = line.split(',')
        if event_group.has_key(res[1]):
            group = event_group[res[1]]
            if user_group.has_key(res[0]):
                groups = user_group[res[0]]
                if group not in groups:
                    '''print 'Not in Group'
                    print 'User:%s, Event:%s.' % (res[0], res[1])
                    print group
                    print groups
                    raw_input()'''
                    outCount += 1
                else:
                    #print 'In group'
                    inCount += 1
    print 'In count: %d.' % inCount
    print 'Out count: %d.' % outCount

def checkDistance(eventLocationFile, userNearEventFile, userEventDisFile):
    '''
    python check.py ../Clean_data/event_lon_lat.csv ../Clean_data/user_near_event.csv ../Clean_data/user_event_di
    '''
    user_location = [-74.0, 40.68]
    event_location_dic = {}
    for line in open(eventLocationFile):
        res = line.strip('\n').split(',')
        event_location_dic[res[0]] = [float(res[1]),float(res[2])]

    wfd = open(userEventDisFile, 'w')
    for line in open(userNearEventFile):
        event_id = line.strip('\n').split(',')[1]
        event_location = map(lambda x: float(x), event_location_dic[event_id])
        dis = distance.distance(user_location, event_location).miles
        if dis > 20:
            print 'Error'
            sys.exit(1)
        wfd.write(str(dis) + '\n')
    wfd.close()

if __name__ == "__main__":
    #checkEventGroup()

    if len(sys.argv) != 4:
        print 'usage: <event_location.in> <user_near_event.in> <user_event_dis.out>'
        sys.exit(1)
    checkDistance(sys.argv[1],sys.argv[2],sys.argv[3])
