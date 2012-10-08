#!/usr/bin/env python
#encoding=utf8

# This script calculate the distance between user's home and group's event
# Output format:
#   userID,groupID,mDis,aDis

'''
python mkHomeEventDis.py ../Clean_Data/NewYork_user_group.csv ../Clean_Data/NewYork_user_lon_lat.csv ../Clean_Data/NewYork_event_group.csv ../Clean_Data/NewYork_event_lon_lat.csv ../Temporal_Data/NewYork_user_group_event_dis.csv
'''
import sys
from geopy import distance

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <user_group_feature.in> <user_location.in> <event_group.in> <event_location.in> <user_group_event_dis.out>'
        sys.exit(1)

    user_locations = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        user_locations[res[0]] = res[1:]

    event_locations = {}
    for line in open(sys.argv[4]):
        res = line.strip('\n').split(',')
        event_locations[res[0]] = res[1:]

    group_event = {}
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        if group_event.has_key(res[1]):
            group_event[res[1]].append(res[0])
        else:
            group_event[res[1]] = [res[0]]

    wfd = open(sys.argv[5], 'w')
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        user_location = user_locations[res[0]]
        min_dis = 1000
        average_dis = 0
        for event_id in group_event[res[1]]:
            event_location = event_locations[event_id]
            dis = distance.distance(map(lambda x: float(x), user_location), map(lambda x: float(x), event_location)).miles
            average_dis += dis
            if min_dis > dis:
                min_dis = dis
        wfd.write("%s,%s,%f,%f\n" % (res[0], res[1], min_dis, average_dis/len(group_event[res[1]])))
    wfd.close()
