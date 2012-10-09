#!/usr/bin/env python
#encoding=utf8

## This script calculate the distance between user's home and other users in target groups.
## It gives the feature file output with the following fields:
#   1.nearest distance between target user and other users in target group
#   2.average distance between target user and other users in target group

'''
python mkHomeHomeDis.py ../Clean_Data/NewYork_user_group.csv ../Clean_Data/user_lon_lat.csv ../Clean_Data/NewYork_user_group.csv ../Temporal_Data/NewYork_user_group_user_dis.temp
'''

import sys
from geopy import distance

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <user_group_feature.in> <user_location.in> <user_group.in> <user_group_user_dis.out>'
        sys.exit(1)

    user_locations = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        user_locations[res[0]] = map(lambda x: float(x), res[1:])

    group_users = {}
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        if group_users.has_key(res[1]):
            group_users[res[1]].append(res[0])
        else:
            group_users[res[1]] = [res[0]]

    wfd = open(sys.argv[4], 'w')
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if not group_users.has_key(res[2]) or not user_locations.has_key(res[1]):
            print 'Not having the group key or the user key.'
            sys.exit(1)

        min_dis = 1000
        average_dis = 0
        num = 0
        for user_id in group_users[res[2]]:
            if user_id != res[1]:
                dis = distance.distance(user_locations[user_id], user_locations[res[1]]).miles
                if dis < min_dis:
                    min_dis = dis
                average_dis += dis
                num += 1

        wfd.write("%s,%f,%f\n" % (line.strip('\n'), min_dis, average_dis/num))
    wfd.close()
