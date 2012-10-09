#!/bin/sh

##This script makes use of many other scripts in "Feature_Generation_Script" to make feature data for training and testing.

# Main procedure:
#   1. Partition raw data
#   2. Sample negative instances of each positive instance
#   3. Combine positive instance and negative instance 
#   4. Make different features for each train instance
#       4.1 make group activeness-based features
#       4.2 make user group relation features
#       4.3 make distance-based features
#           4.3.1 distance between user's home and target group's event
# @author: anthonylife
# @date: 10/8/2012


## Global parameters setting
#===========================

# directory path setting
ScriptRootPath="Feature_Generation_Script"
FeatureRootPath="Features"
DataRootPath="Clean_Data"
TrainDataRootPath="Train_Test_Data"

# number of data sets
PartitionNum=5

# ratio of the number of training data and test data
Ratio=0.8
# ratio of the number of negative and positive instances in training data
RatioPN=4


# 1. Partition raw data
#python $ScriptRootPath/rPartition.py $DataRootPath/NewYork_user_group.csv $PartitionNum $TrainDataRootPath/NewYork_user_group.pos

# 2. Sample negative instances of each positive instance
#python $ScriptRootPath/getNegInstance.py $DataRootPath/NewYork_user_group.csv $DataRootPath/NewYork_group.csv $TrainDataRootPath  $RatioPN NewYork_user_group.pos

# 3. Combine positive instance and negative instance 
#python $ScriptRootPath/mergePoNeIns.py $TrainDataRootPath 'pos,neg' 5 $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv

# 4. Make different features for each train instance
#   4.1 make group activeness-based features
#python $ScriptRootPath/mkGroupActiveFeatures.py $TrainDataRootPath/NewYork_user_group.train.csv $DataRootPath/NewYork_event_group.csv $DataRootPath/NewYork_event_lon_lat.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv $FeatureRootPath/NewYork_group_activeness.features.csv

#   4.2 make user group relation features
#python $ScriptRootPath/mkUGRelation.py $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv $FeatureRootPath/NewYork_user_group_sim.features.csv

#   4.3 make distance-based features
#       4.3.1 distance between user's home and target group's event
#python $ScriptRootPath/mkHomeEventDis.py $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_lon_lat.csv $DataRootPath/NewYork_event_group.csv $DataRootPath/NewYork_event_lon_lat.csv $FeatureRootPath/NewYork_user_group_event_dis.features.csv
#       4.3.2 distance between user's home and home of users in target group
#python $ScriptRootPath/mkHomeHomeDis.py $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_lon_lat.csv $DataRootPath/NewYork_user_group.csv $FeatureRootPath/NewYork_user_group_user_dis.features.csv
#       4.3.3 distance between the locations of the events user joined and the events in target groups
python $ScriptRootPath/mkEventEventDis.py $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_event.csv $DataRootPath/NewYork_event_lon_lat.csv $DataRootPath/NewYork_event_group.csv $FeatureRootPath/NewYork_event_group_event_dis.features.csv
#       4.3.4 distance between the locations of events the user joined and locations of other users in target groups
python $ScriptRootPath/mkEventHomeDis.py $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_event.csv $DataRootPath/NewYork_event_lon_lat.csv $TrainDataRootPath/NewYork_user_group.train.csv $DataRootPath/NewYork_user_lon_lat.csv $DataRootPath/NewYork_event_group.csv $FeatureRootPath/NewYork_event_group_home_dis.features.csv
