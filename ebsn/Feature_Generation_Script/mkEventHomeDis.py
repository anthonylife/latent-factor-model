#!/usr/bin/env python
#encoding=utf8

## This script calculate the distance between the events user joined and locations of users in target groups.
## It gives the feature file output with the following fields:
#   1.nearest distance between events of target user and locations of users in target group
#   2.average distance between events of target user and locations of target users in target group

'''
python mkEventHomeDis.py ../Clean_Data/NewYork_user_group.csv ../Clean_Data/NewYork_user_event.csv ../Clean_Data/NewYork_event_lon_lat.csv ../Clean_Data/NewYork_user_group.csv ../Clean_Data/NewYork_user_lon_lat.csv ../Temporal_Data/NewYork_event_group_user_dis.csv
'''

import sys
from geopy import distance

def calAverageDis(events, events_locations, users, user_locations):
    event_mean_loc = [0, 0]
    for event_id in events:
        event_mean_loc = [event_mean_loc[i]+event_locations[event_id][i] for i in xrange(2)]
    event_mean_loc= [event_mean_loc[i]/len(events) for i in xrange(2)]

    user_mean_loc = [0, 0]
    for user_id in users:
        user_mean_loc = [user_mean_loc[i] + user_locations[user_id][i] for i in xrange(2)]
    user_mean_loc = [user_mean_loc[i]/len(users) for i in xrange(2)]

    return distance.distance(event_mean_loc, user_mean_loc).miles

def calMinDis(events, events_locations, users, user_locations):
    min_dis = 1000
    for event_id in events:
        for user_id in users:
            dis = distance.distance(event_locations[event_id], user_locations[user_id]).miles
            if dis < min_dis:
                min_dis = dis
    return min_dis

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print 'usage: <user_group_feature.in> <user_event.in> <event_location.in> <user_group.in> <user_location.in> <event_group_event_dis.out>'
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

    group_users = {}
    for line in open(sys.argv[4]):
        res = line.strip('\n').split(',')
        if group_users.has_key(res[1]):
            group_users[res[1]].append(res[0])
        else:
            group_users[res[1]] = [res[0]]

    user_locations = {}
    for line in open(sys.argv[5]):
        res = line.strip('\n').split(',')
        user_locations[res[0]] = map(lambda x: float(x), res[1:])

    wfd = open(sys.argv[6], 'w')
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        average_dis = calAverageDis(user_events[res[0]], event_locations, group_users[res[1]], user_locations)
        min_dis = calMinDis(user_events[res[0]], event_locations, group_users[res[1]], user_locations)
        wfd.write("%s,%s,%f,%f\n" % (res[0], res[1], min_dis, average_dis))
    wfd.close()
