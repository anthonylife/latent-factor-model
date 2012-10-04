#!/usr/bin/sh

##This is a script for filtering data based on the following principles:
#   Two parts: 1-->whether specified property existed? 2-->iterative filtering on changingfrequency
#   1.
#       1.1 Filter the tag list the first time(text rule)   --> "tag_clean.py"
#       1.2 Filter the users, groups and events not having location addresses  --> "filterEventLocation.py", "filterUserLocation.py"
#   2. Iterative filtering because the condition of items' frequency changing. Following are global conditions  --> "filterUserGroupFreq.py"
#       2.1 User should attend at least 5 groups. Temporarily, don't considering the events and tags
#       2.2 Group should have at least 5 users. Temporarily, don't considering the events and tags
#   3. After getting the final list of users and groups, filter other information using these lists.  --> "filterByOneItem.py", "filterByTwoItem.py", "getTagFreq.py", "filterTagByFreq.py"
#
#   Ouput: output cleaned data, including users
#
#   @author: anthonlife
#   @Created Date: 9/30/2012


## Initial Setting
RootPath="Pre_Process_Script"

## 1. Tag cleaning and location filtering
python ./$RootPath/tagClean.py
python filterEventLocation.py ../Meetup_geo/event_lon_lat.csv ../Meetup_network/event_group.csv ../Temporal_Data/user_event.temp.1 ../Temporal_Data/event_group.1 ../Temporal_Data/user_event.temp.2

## 2. Iterative filtering user and groups by frequency
python filterUserGroupFreq.py ../Temporal_Data/user_group.temp.1 ../Temporal_Data/user.temp.1 ../Temporal_Data/group.temp.1

## 3. Filter other information
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Temporal_Data/user_event.temp.2 0 ../Clean_data/user_event.csv
python filterByOneItem.py ../Temporal_Data/group.temp.1 ../Temporal_Data/event_group.temp.1 1 ../Clean_data/event_group.csv
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Meetup_geo/user_lon_lat.csv 0 ../Clean_data/user_lon_lat.csv
python filterByOneItem.py ../Temporal_Data/user.temp.1 ../Meetup_tag/user_tag.new 0 ../Temporal_Data/user_tag.temp.1
python filterByOneItem.py ../Temporal_Data/group.temp.1 ../Meetup_tag/group_tag.new 0 ../Temporal_Data/group_tag.temp.1
python filterByOneItem.py ../Temporal_Data/event.temp.1 ../Meetup_geo/event_lon_lat.csv 0 ../Clean_data/event_lon_lat.csv
python filterByTwoItem.py ../Temporal_Data/user.temp.1 ../Temporal_Data/group.temp.1 ../Temporal_Data/user_group.temp.1 0 1 ../Clean_data/user_group.csv
python getTagFreq.py ../Temporal_Data/user_tag.temp.1 ../Temporal_Data/group_tag.temp.1 ../Sta_Data/tag_freq.sta ../Temporal_data/tag.temp.1
python filterTagByFreq.py ../Temporal_Data/tag.temp.1 ../Temporal_Data/user_tag.temp.1 ../Temporal_Data/group_tag.temp.1 ../Clean_data/user_tag.csv ../Clean_data/group_tag.csv

# New generated data for specified locations 
# ==========================================
# 1. Get city level users
python getCityLevelUser.py ../Clean_data/user_lon_lat.csv ../Clean_data/NewYork_user.csv
python getCityLevelUser.py ../Clean_data/user_lon_lat.csv ../Clean_data/London_user.csv

# 2. Filter groups accroding to the city user list
python filterByOneItem.py ../Temporal_data/NewYork_user.temp ../Temporal_Data/user_group.temp.1 0 ../Temporal_Data/NewYork_user_group.temp
python filterByOneItem.py ../Temporal_Data/LosAngeles_user.temp ../Temporal_Data/user_group.temp.1 0 ../Temporal_Data/LosAngeles_user_group.temp

# 3. Iterative filtering user and groups by frequency
python filterUserGroupFreq.py ../Temporal_Data/NewYork_user_group.temp ../Temporal_Data/NewYork_user.temp.1 ../Temporal_Data/NewYork_group.temp.1
python filterUserGroupFreq.py ../Temporal_Data/LosAngeles_user_group.temp ../Temporal_Data/LosAngeles_user.temp.1 ../Temporal_Data/LosAngeles_group.temp.1

# 4. Filter user-event, event-group information
python filterByOneItem.py ../Temporal_Data/NewYork_user.temp.1 ../Temporal_Data/user_event.temp.2 0 ../Clean_data/NewYork_user_event.csv
python filterByOneItem.py ../Temporal_Data/LosAngeles_user.temp.1 ../Temporal_Data/user_event.temp.2 0 ../Clean_data/LosAngeles_user_event.csv
python filterByOneItem.py ../Temporal_Data/NewYork_group.temp.1 ../Temporal_Data/event_group.temp.1 1 ../Clean_data/NewYork_event_group.csv
python filterByOneItem.py ../Temporal_Data/LosAngeles_group.temp.1 ../Temporal_Data/event_group.temp.1 1 ../Clean_data/LosAngeles_event_group.csv

# 5. Filter other information 
python filterByOneItem.py ../Temporal_Data/NewYork_user.temp.1 ../Meetup_geo/user_lon_lat.csv 0 ../Clean_data/NewYork_user_lon_lat.csv
python filterByOneItem.py ../Temporal_Data/LosAngeles_user.temp.1 ../Meetup_geo/user_lon_lat.csv 0 ../Clean_data/LosAngeles_user_lon_lat.csv
python filterByOneItem.py ../Temporal_Data/NewYork_user.temp.1 ../Meetup_tag/user_tag.new 0 ../Temporal_Data/NewYork_user_tag.temp.1
python filterByOneItem.py ../Temporal_Data/LosAngeles_user.temp.1 ../Meetup_tag/user_tag.new 0 ../Temporal_Data/LosAngeles_user_tag.temp.1
python filterByOneItem.py ../Temporal_Data/NewYork_group.temp.1 ../Meetup_tag/group_tag.new 0 ../Temporal_Data/NewYork_group_tag.temp.1
python filterByOneItem.py ../Temporal_Data/LosAngeles_group.temp.1 ../Meetup_tag/group_tag.new 0 ../Temporal_Data/LosAngeles_group_tag.temp.1
python filterByOneItem.py ../Temporal_Data/NewYork_event.temp.1 ../Meetup_geo/event_lon_lat.csv 0 ../Clean_data/NewYork_event_lon_lat.csv
python filterByOneItem.py ../Temporal_Data/LosAngeles_event.temp.1 ../Meetup_geo/event_lon_lat.csv 0 ../Clean_data/LosAngeles_event_lon_lat.csv


python filterByTwoItem.py ../Temporal_Data/NewYork_user.temp.1 ../Temporal_Data/NewYork_group.temp.1 ../Temporal_Data/user_group.temp.1 0 1 ../Clean_data/NewYork_user_group.csv
python filterByTwoItem.py ../Temporal_Data/LosAngeles_user.temp.1 ../Temporal_Data/LosAngeles_group.temp.1 ../Temporal_Data/user_group.temp.1 0 1 ../Clean_data/LosAngeles_user_group.csv
python getTagFreq.py ../Temporal_Data/NewYork_user_tag.temp.1 ../Temporal_Data/NewYork_group_tag.temp.1 ../Sta_Data/NewYork_tag_freq.sta ../Temporal_Data/NewYork_tag.temp.1
python getTagFreq.py ../Temporal_Data/LosAngeles_user_tag.temp.1 ../Temporal_Data/LosAngeles_group_tag.temp.1 ../Sta_Data/LosAngeles_tag_freq.sta ../Temporal_Data/LosAngeles_tag.temp.1
python filterTagByFreq.py ../Temporal_Data/NewYork_tag.temp.1 ../Temporal_Data/NewYork_user_tag.temp.1 ../Temporal_Data/NewYork_group_tag.temp.1 ../Clean_data/NewYork_user_tag.csv ../Clean_data/NewYork_group_tag.csv
python filterTagByFreq.py ../Temporal_Data/LosAngeles_tag.temp.1 ../Temporal_Data/LosAngeles_user_tag.temp.1 ../Temporal_Data/LosAngeles_group_tag.temp.1 ../Clean_data/LosAngeles_user_tag.csv ../Clean_data/LosAngeles_group_tag.csv

python filterByOneItem.py ../Clean_data/NewYork_event.csv ../Clean_data/NewYork_user_event.csv 1 ../Clean_data/NewYork_user_event.csv1
python filterByOneItem.py ../Clean_data/LosAngeles_event.csv ../Clean_data/LosAngeles_user_event.csv 1 ../Clean_data/LosAngeles_user_event.csv1

