#!/user/bin/env python
#encoding=utf-8

## This script generate the addr of the events user joined
## Create: 2012/9/20
## Last Modified: 2012/9/20

import sys

# Input file path initialization
Event_addr_file = '../Meetup_geo/event_lon_lat.csv'
User_addr_file = "../Meetup_geo/user_lon_lat.csv"
User_event_file = '../Sta_Data/user_join_event.csv'

# Output file path
User_event_addr_file = "../Sta_Data/user_event_addr.csv"

# Start
if __name__ == "__main__":
    User_addr = {}  # User address dic
    #print "Start 1"
    index = 1
    for line in open(User_addr_file):
        ele = line.split(',')
        index = index + 1
        #print index
        User_addr[ele[0]] = [ele[1], ele[2]]
    #print "Finish 1"
    Event_addr = {}
    #print "Start 2"
    index = 1
    for line in open(Event_addr_file):
        ele = line.split(',')
        index = index + 1
        #print index
        Event_addr[ele[0]] = [ele[1], ele[2]]

    #print "Finish 2"
    cache = 0
    for line in open(User_event_file):
        ele = line.split(',')
        ele[1] = ele[1].strip('\n')
        if User_addr.has_key(ele[0]):
            if ele[0] != cache:
                sys.stdout.write(str(ele[0]) + '\n')
                sys.stdout.write(str(User_addr[ele[0]][0]) + ',' + str(User_addr[ele[0]][1]))
                cache = ele[0]
            if Event_addr.has_key(ele[1]):
                sys.stdout.write(str(Event_addr[ele[1]][0]) + ',' + str(Event_addr[ele[1]][1]))

