#!/usr/bin/env python
#encoding=utf8

'''
python filterEventLocation.py ../Meetup_geo/event_lon_lat.csv ../Meetup_network/event_group.csv ../Temporal_Data/user_event.temp.1 ../Temporal_Data/event_group.1 ../Temporal_Data/user_event.temp.2


'''

import sys

def processFile(eventdic, inputFile, outputFile, sitem):
    wfd = open(outputFile, 'w')
    for line in open(inputFile):
        event = line.strip('\n').split(',')[sitem-1]
        if eventdic.has_key(event):
            wfd.write(line)
    wfd.close()

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <user_location.in> <user_group.in> <user_event.in> <user_tag.in> <user_group.out> <user_event.out> <user_tag.out>'
        sys.exit(1)

    # Create dictionary of users having location
    eventdic = {}
    for line in open(sys.argv[1]):
        event = line.strip('\n').split(',')[0]
        if eventdic.has_key(event):
            print 'Event key repeated.'
            sys.exit(1)
        else:
            eventdic[event] = 1

    processFile(eventdic, sys.argv[2], sys.argv[4], 1)
    processFile(eventdic, sys.argv[3], sys.argv[5], 2)

