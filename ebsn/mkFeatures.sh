#!/bin/sh

##This script makes use of many other scripts in "Feature_Generation_Script" to make feature data for training and testing.

# Main procedures:
#   0. Reindex all data
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

## Runing procedures
# 1.Reindex all data
#echo 'Reindex all data...'
#python $ScriptRootPath/reIndex.py $DataRootPath/NewYork_user.csv $DataRootPath/NewYork_group.csv $DataRootPath/NewYork_tag.csv $DataRootPath/NewYork_event.csv $DataRootPath/NewYork_event_group.csv $DataRootPath/NewYork_group_tag.csv $DataRootPath/NewYork_tag_text.csv $DataRootPath/NewYork_user_event.csv $DataRootPath/NewYork_user_group.csv $DataRootPath/NewYork_user_lon_lat.csv $DataRootPath/NewYork_user_tag.csv $DataRootPath/NewYork_event_lon_lat.csv $DataRootPath/NewYork_user.ridx.csv $DataRootPath/NewYork_group.ridx.csv $DataRootPath/NewYork_tag.ridx.csv $DataRootPath/NewYork_event.ridx.csv $DataRootPath/NewYork_event_group.ridx.csv $DataRootPath/NewYork_group_tag.ridx.csv $DataRootPath/NewYork_tag_text.ridx.csv $DataRootPath/NewYork_user_event.ridx.csv $DataRootPath/NewYork_user_group.ridx.csv $DataRootPath/NewYork_user_lon_lat.ridx.csv $DataRootPath/NewYork_user_tag.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv

# 2. Randomly partition train data and test data
echo 'Randomly partition train data and test data accroding to specified ratio...'
python $ScriptRootPath/rSample.py $DataRootPath/NewYork_user_group.ridx.csv $Ratio $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/ NewYork_user_group.test.csv
cp $TrainDataRootPath/NewYork_user_group.train.csv $FeatureRootPath/NewYork_user_group.train.csv
cp $TrainDataRootPath/NewYork_user_group.test.csv $FeatureRootPath/NewYork_user_group.test.csv

# 3. Sample negative instances of each positive instance and segment them into train and test data
echo 'Sample negative instances of each positive instance...'
python $ScriptRootPath/getNegInstance.py $DataRootPath/NewYork_user_group.ridx.csv $DataRootPath/NewYork_group.ridx.csv $TrainDataRootPath/NewYork_user_group.train.csv $RatioPN $TrainDataRootPath/NewYork_rate_user_group.train.csv
python $ScriptRootPath/getNegInstance.py $DataRootPath/NewYork_user_group.ridx.csv $DataRootPath/NewYork_group.ridx.csv $TrainDataRootPath/NewYork_user_group.test.csv $RatioPN $TrainDataRootPath/NewYork_rate_user_group.test.csv
cp $TrainDataRootPath/NewYork_rate_user_group.train.csv $FeatureRootPath/NewYork_rate_user_group.train.csv
cp $TrainDataRootPath/NewYork_rate_user_group.test.csv $FeatureRootPath/NewYork_rate_user_group.test.csv

# 4. Make different features for each train instance
#   4.1 make group activeness-based features
echo 'make group activeness-based features...'
python $ScriptRootPath/mkGroupActiveFeatures.py $TrainDataRootPath/NewYork_user_group.train.csv $DataRootPath/NewYork_event_group.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv $FeatureRootPath/NewYork_group_activeness.train.features.csv
python $ScriptRootPath/mkGroupActiveFeatures.py $TrainDataRootPath/NewYork_user_group.train.csv $DataRootPath/NewYork_event_group.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $TrainDataRootPath/NewYork_rate_user_group.test.csv $FeatureRootPath/NewYork_group_activeness.test.features.csv

#   4.2 make user group relation features
echo 'make user group relation features...'
python $ScriptRootPath/mkUGRelation.py $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_event.ridx.csv $DataRootPath/NewYork_group_event.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $FeatureRootPath/NewYork_user_group_sim_ps.train.features.csv $FeatureRootPath/NewYork_user_group_sim_loc.train.features.csv
python $ScriptRootPath/mkUGRelation.py $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.test.csv $DataRootPath/NewYork_user_event.ridx.csv $DataRootPath/NewYork_group_event.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $FeatureRootPath/NewYork_user_group_sim_ps.test.features.csv $FeatureRootPath/NewYork_user_group_sim_loc.test.features.csv

#   4.3 make distance-based features
#       4.3.1 distance between user's home and target group's event
echo 'distance between user's home and target group's event...'
python $ScriptRootPath/mkHomeEventDis.py $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_lon_lat.ridx.csv $DataRootPath/NewYork_event_group.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $FeatureRootPath/NewYork_user_group_event_dis.train.features.csv
python $ScriptRootPath/mkHomeEventDis.py $TrainDataRootPath/NewYork_user_group.train.csv $TrainDataRootPath/NewYork_rate_user_group.test.csv $DataRootPath/NewYork_user_lon_lat.ridx.csv $DataRootPath/NewYork_event_group.ridx.csv $DataRootPath/NewYork_event_lon_lat.ridx.csv $FeatureRootPath/NewYork_user_group_event_dis.test.features.csv

#       4.3.2 distance between user's home and home of users in target group
echo "distance between user's home and home of users in target group..."
python $ScriptRootPath/mkHomeHomeDis.py $TrainDataRootPath/NewYork_rate_user_group.train.csv $DataRootPath/NewYork_user_lon_lat.ridx.csv $DataRootPath/NewYork_user_group.ridx.csv $FeatureRootPath/NewYork_user_group_user_dis.train.features.csv
python $ScriptRootPath/mkHomeHomeDis.py $TrainDataRootPath/NewYork_rate_user_group.test.csv $DataRootPath/NewYork_user_lon_lat.ridx.csv $DataRootPath/NewYork_user_group.ridx.csv $FeatureRootPath/NewYork_user_group_user_dis.test.features.csv

# 5. Combine different feature files into one file
echo "Combine different feature files into one file..."
python $ScriptRootPath/combineFeatures.py $FeatureRootPath/NewYork_group_activeness.train.features.csv $FeatureRootPath/NewYork_user_group_sim_ps.train.features.csv $FeatureRootPath/NewYork_user_group_sim_dis.train.features.csv $FeatureRootPath/NewYork_user_group_event_dis.train.features.csv $FeatureRootPath/NewYork_user_group_user_dis.train.features.csv $RatioPN $FeatureRootPath/NewYork_train_all.features.csv
python $ScriptRootPath/combineFeatures.py $FeatureRootPath/NewYork_group_activeness.test.features.csv $FeatureRootPath/NewYork_user_group_sim_ps.test.features.csv $FeatureRootPath/NewYork_user_group_sim_dis.test.features.csv $FeatureRootPath/NewYork_user_group_event_dis.test.features.csv $FeatureRootPath/NewYork_user_group_user_dis.test.features.csv $RatioPN $FeatureRootPath/NewYork_test_all.features.csv

