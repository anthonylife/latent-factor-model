#!/usr/bin/env python
#encoding=utf8

# This script extract list of users in specified cities
'''
python getCityLevelUser.py ../Clean_data/user_lon_lat.csv ../Clean_data/NewYork_user.csv
python getCityLevelUser.py ../Clean_data/user_lon_lat.csv ../Clean_data/London_user.csv
'''


import sys
from geopy import distance

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <user_lon_lat.in> <user_city.out> <city_tag.in>'
        sys.exit(1)

    # Location longitude, latitude and radius
    if sys.argv[3] == '1':
        [city_location, radius]= [[40.43, -74], 20]   # NewYork
    #[city_location, radius]= [[51.3025, -0.0739], 20]   # London
    #[city_location, radius]= [[35.412222, 139.413012], 20]   # Tokyo
    elif sys.argv[3] == '2':
        [city_location, radius]= [[34.03, -118.14], 20]   # Los Angeles

    # Load all user coordinates
    user_coor_dic = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        user_coor_dic[res[0]] = [float(res[2]), float(res[1])]  #Order: latitude and longtitude

    # Get the city user list
    wfd = open(sys.argv[2], 'w')
    for user_id in user_coor_dic.keys():
        if distance.distance(user_coor_dic[user_id], city_location).miles < radius:
            wfd.write("%s,%s,%s\n" % (user_id, str(user_coor_dic[user_id][1]), str(user_coor_dic[user_id][0])))
    wfd.close()
