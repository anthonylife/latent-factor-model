#!/usr/bin/env python
#encoding=utf8

## This script combine all features of train instances into one unified feature file.

#  Feature format is based the specified rule in README file.
#  Format for matlab: user_id;pos_group_id;neg_group_id;pos_group_activeness_based features;
#                     neg_group_activeness_based features;pos_user_group_relation features;
#                     neg_user_group_relation;pos_distance_based features;neg_distance_based features
#  @author: anthonylife
#  @date: 10/8/2012

import sys
import random

def fillFeatures(user_group_features, res, explicit_feature_idx, group_id):
    if res[0] == '1':
        features_cache = user_group_features[res[1]][1]
    elif res[0] == '0':
        features_cache = user_group_features[res[1]][0]
    else:
        print 'instance class error.'
        sys.exit(1)
    if group_id not in features_cache:
        features_cache[group_id] = []
    for i,feature in enumerate(res[3:]):
        features_cache[group_id].append(str(explicit_feature_idx+i)+":"+feature)

def formatFeatures(user, pos_features, neg_features):
    all_feature = user + ";" + pos_features[0] + ";" + neg_features[0] + ";"
    all_feature += ' '.join(pos_features[1]) + ";"
    all_feature += ' '.join(neg_features[1]) + '\n'
    return all_feature

if __name__ == "__main__":
    if len(sys) != 9:
        print 'usage: <group_activeness_features.in> <user_group_relation_features.in> <home_event_dis_features.in> <home_home_dis_features.in> <event_event_dis_features.in> <event_home_dis_features.in> <ratio.in> <unified_features.out>'
        sys.exit(1)

    explicit_feature_idx = 1    # feature index
    user_group_features = {}
    # activeness features
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if res[1] not in user_group_features:
            user_group_features[res[1]] = [{}, {}]
        fillFeatures(user_group_features, res, explicit_feature_idx, res[2])
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # relation features
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        fillFeatures(user_group_features, res, explicit_feature_idx)
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # home-event distance features
    for line in open(sys.argv[3]):
        res = line.strip('\n').split(',')
        fillFeatures(user_group_features, res, explicit_feature_idx)
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # home-home distance features
    for line in open(sys.argv[4]):
        res = line.strip('\n').split(',')
        fillFeatures(user_group_features, res, explicit_feature_idx)
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # event-event distance features
    for line in open(sys.argv[5]):
        res = line.strip('\n').split(',')
        fillFeatures(user_group_features, res, explicit_feature_idx)
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # event-home distance features
    for line in open(sys.argv[6]):
        res = line.strip('\n').split(',')
        fillFeatures(user_group_features, res, explicit_feature_idx)
    explicit_feature_idx = len(user_group_features.values[0].values[0])+1

    # construct pos-neg train instance pairs and shuffle
    ratio_pos_neg = int(sys.argv[7])
    train_ins_features = []
    for user in user_group_features:
        if len(user_group_features[user][0]) != ratio_pos_neg*len(user_group_features[user][1]):
            print 'Sample ratio error.'
            sys.exit(1)
        pos_ins_features = user_group_features[user][1].items()
        neg_ins_features = user_group_features[user][0].items()
        for i in xrange(len(neg_ins_features)):
            train_ins_features.append(formatFeatures(user, pos_ins_features[i/ratio_pos_neg], neg_ins_features[i]))

    random.shuffle(train_ins_features)
    # output
    wfd = open(sys.argv[8], 'w')
    for ins in train_ins_features:
        wfd.write(ins)
    wfd.close()
