#!/usr/bin/env python
#encoding=utf8

# This script used for generating group-based features

'''
python mkGroupActiveFeatures.py ../Clean_data/NewYork_user_group.csv ../Clean_data/NewYork_event_group.csv ../Clean_data/NewYork_event_lon_lat.csv ../Temporal_Data/NewYork_group_active_features.csv
'''

import sys

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <user_group.in> <event_group.in> <event_addr.in> <group_activeness_features.out>'
        sys.exit(1)

    group_features = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if group_features.has_key(res[1]):
            group_features[res[1]][0] += 1
        else:
            group_features[res[1]] = [1, 0, 0]  #[0]: num of users; [1]: num of events; [2]: num of locations

    event_addr = {}
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        event_addr[res[0]] = [res[1], res[2]]

    group_addr = {}
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        group_features[res[1]][1] += 1
        if group_addr.has_key(res[1]):
            group_addr[res[1]].append(event_addr[res[0]][0] + '_' + event_addr[res[0]][0])
        else:
            group_addr[res[1]] = [event_addr[res[0]][0] + '_' + event_addr[res[0]][0]]

    wfd = open(sys.argv[4], 'w')
    for key in group_addr.keys():
        group_features[key][2] = len(set(group_addr[key]))
        wfd.write("%s,%d,%d,%d\n" % (key, group_features[key][0], group_features[key][1], group_features[key][2]))
    wfd.close()
