#!/usr/bin/env python
#encoding=utf8

# This script filters groups without having at least an event which has location

import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <event_location.in> <event_group.in> <user_group.in> <user_group.out>'
        sys.exit(1)

    event_locations = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        event_locations[res[0]] = 0

    groups = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        if event_locations.has_key(res[0]):
            groups[res[1]] = 0

    wfd = open(sys.argv[4], 'w')
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        if groups.has_key(res[1]):
            wfd.write(line)
    wfd.close()

