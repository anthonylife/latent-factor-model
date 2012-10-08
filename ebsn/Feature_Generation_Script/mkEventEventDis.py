#!/usr/bin/env python
#encoding=utf8

## This script calculate the distance between the events user joined and events in target groups.
## It gives the feature file output with the following fields:
#   1.nearest distance between events of target user and events in target group
#   2.average distance between events of target user and events in target group

'''
python mkEventEventDis.py ../Clean_Data/NewYork_user_group.csv ../Clean_Data/NewYork_user_event.csv ../Clean_Data/NewYork_event_lon_lat.csv ../Clean_Data/NewYork_event_group.csv ../Temporal_Data/NewYork_event_group_event_dis.csv
'''

import sys
from geopy import distance

def calAverageDis(user_event, group_event, event_locations):
    user_mean_loc = [0, 0]
    for event_id in user_event:
        user_mean_loc = [user_mean_loc[i]+event_locations[event_id][i] for i in xrange(2)]
    user_mean_loc= [user_mean_loc[i]/len(user_event) for i in xrange(2)]

    group_mean_loc = [0, 0]
    for event_id in group_event:
        group_mean_loc = [group_mean_loc[i] + event_locations[event_id][i] for i in xrange(2)]
    group_mean_loc = [group_mean_loc[i]/len(group_event) for i in xrange(2)]

    return distance.distance(user_mean_loc, group_mean_loc).miles

def calMinDis(user_event, group_event, event_locations):
    min_dis = 1000
    for event_1 in user_event:
        for event_2 in group_event:
            dis = distance.distance(event_locations[event_1], event_locations[event_2]).miles
            if dis < min_dis:
                min_dis = dis
    return min_dis

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print 'usage: <user_group_feature.in> <user_event.in> <event_location.in> <event_group.in> <event_group_event_dis.out>'
        sys.exit(1)

    user_events = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        if user_events.has_key(res[0]):
            user_events[res[0]].append(res[1])
        else:
            user_events[res[0]] = [res[1]]

    event_locations = {}
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        event_locations[res[0]] = map(lambda x: float(x), res[1:])

    group_events = {}
    for line in open(sys.argv[4]):
        res = line.strip('\n').split(',')
        if group_events.has_key(res[1]):
            group_events[res[1]].append(res[0])
        else:
            group_events[res[1]] = [res[0]]

    wfd = open(sys.argv[5], 'w')
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if not group_events.has_key(res[1]) or not user_events.has_key(res[0]):
            print 'Not having the group key or user key: group->%s, user->%s' % (res[1], res[0])
            sys.exit(1)
        average_dis = calAverageDis(user_events[res[0]], group_events[res[1]], event_locations)
        min_dis = calMinDis(user_events[res[0]], group_events[res[1]], event_locations)
        wfd.write("%s,%s,%f,%f\n" % (res[0], res[1], min_dis, average_dis))
    wfd.close()
