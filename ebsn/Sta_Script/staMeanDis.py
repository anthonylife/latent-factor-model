#!/usr/bin/env python
#encoding=utf8
import sys
from geopy import distance

'''
python staMeanDis.py ../Clean_data/NewYork_event_lon_lat.csv ../Clean_data/NewYork_user_lon_lat.csv ../Clean_data/NewYork_user_event.csv ../Sta_Data/event_influence_dis.csv
'''

minNumUser = 5

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <event_addr.in> <user_addr.in> <user_event.in> <event_influenc_dis.out>'
        sys.exit(1)

    event_geo_dic = {}
    user_geo_dic = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        event_geo_dic[res[0]] = [float(res[2]), float(res[1])]

    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        user_geo_dic[res[0]] = [float(res[2]), float(res[1])]

    event_influence_dic = {}
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        mile = distance.distance(event_geo_dic[res[1]], user_geo_dic[res[0]]).miles
        if event_influence_dic.has_key(res[1]):
            event_influence_dic[res[1]][0] += 1
            event_influence_dic[res[1]][1] += mile
        else:
            event_influence_dic[res[1]]= [1, mile]

    wfd = open(sys.argv[4], 'w')
    for event_id in event_influence_dic.keys():
        if event_influence_dic[event_id][0] > minNumUser:
            wfd.write('%s,%f\n' % (event_id, event_influence_dic[event_id][1]*1.0/event_influence_dic[event_id][0]))
        else:
            wfd.write('%s,0\n' % event_id)
    wfd.close()
