#!/usr/bin/env python
#encoding=utf8

import sys

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

if __name__ == "__main__":
    checkEventGroup()
