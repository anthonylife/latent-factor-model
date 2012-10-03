#!/usr/bin/env python
#encoding=utf8

'''
python filterLocation.py ../Meetup_geo/user_lon_lat.csv ../Meetup_network/user_group.csv ../Meetup_network/user_event.csv ../Meetup_tag/user_tag.new ../Temporal_Data/user_group.temp.1 ../Temporal_Data/user_event.temp.1 ../Temporal_Data/user_tag.temp.1


'''

import sys

def processFile(userdic, inputFile, outputFile):
    wfd = open(outputFile, 'w')
    for line in open(inputFile):
        user = line.strip('\n').split(',')[0]
        if userdic.has_key(user):
            wfd.write(line)
    wfd.close()

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print 'usage: <user_location.in> <user_group.in> <user_event.in> <user_tag.in> <user_group.out> <user_event.out> <user_tag.out>'
        sys.exit(1)

    # Create dictionary of users having location
    userdic = {}
    for line in open(sys.argv[1]):
        user = line.strip('\n').split(',')[0]
        if userdic.has_key(user):
            print 'User key repeated.'
            sys.exit(1)
        else:
            userdic[user] = 1

    processFile(userdic, sys.argv[2], sys.argv[5])
    processFile(userdic, sys.argv[3], sys.argv[6])
    processFile(userdic, sys.argv[4], sys.argv[7])
