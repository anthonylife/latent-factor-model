#!/usr/bin/env python
#encoding=utf8

import sys
from geopy import distance

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <user_event.in> <user_addr.in> <event_addr.in> <user_event_dis.out>'
        sys.exit(1)

    user_location = {}
    for line in open(sys.argv[2]):
        line = line.strip('\n')
        res = line.split(',')
        if user_location.has_key(res[0]):
            print 'user id duplicated.'
            sys.exit(1)
        else:
            user_location[res[0]] = res[1:]
    print 'load user location finish'

    event_location = {}
    for line in open(sys.argv[3]):
        line = line.strip('\n')
        res = line.split(',')
        if event_location.has_key(res[0]):
            print 'event id duplicated.'
            sys.exit(1)
        else:
            event_location[res[0]] = res[1:]
    print 'load event location finish'

    wfd = open(sys.argv[4], 'w')
    for line in open(sys.argv[1]):
        [user, event] = line.strip('\n').split(',')
        if user_location.has_key(user):
            user_lon_ln = user_location[user]
            if event_location.has_key(event):
                event_lon_ln = event_location[event]
                miles = distance.distance(user_lon_ln, event_lon_ln).miles
                wfd.write("%s,%s,%s\n" % (user, event, str(miles)))
    wfd.close()

