#!/usr/bin/env python
#encoding=utf8

# This script filters city-level users who haven't join events with locations.

import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <event_location.in> <user.in> <user_event.in> <user.out>'
        sys.exit(1)

    event_locations = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        event_locations[res[0]] = 0

    users = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        users[res[0]] = 0     # 0: having no events with locations

    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        if event_locations.has_key(res[1]) and users.has_key(res[0]):
            users[res[0]] = 1

    wfd = open(sys.argv[4], 'w')
    for user_id in users.keys():
        if users[user_id] == 1:
            wfd.write("%s\n" % (user_id))
    wfd.close()
