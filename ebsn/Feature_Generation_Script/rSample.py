#!/usr/bin/env python
#encoding=utf8

# This script can the input file by line into specified number of parts.
# Note: Sampling process of train and test set partition should satisfy the following requirement:
#       ---- Every user and group should occur at least one time in training data set.
#   In order to obey the above rule, I adopt the following method:
#       1.Create two dictionaries, one using "user" as key and the other using "group" as key.
#       2.Loops over user keys and for each key, sample one group as training data. After finishing
#           this process, we can ensure every user id will occur in train data.
#       3.Check whether every group id occured in train data. For group id not occuring in train
#           data, sample one user as training data. After doing this, we can assure every group
#           id will occur in train data.
#       4.For the left data, randomly partition them into train and test data accroding to the
#           specified ratio.

'''
python Feature_Generation_Script/rSample.py Clean_Data/NewYork_user_group.ridx.csv 0.8 Train_Test_Data/NewYork_user_group.train.csv Train_Test_Data/NewYork_user_group.test.csv
'''

import sys
import random
from math import ceil

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print 'usage: <file.in> <samples_num.in> <train_file.out> <test_file.out>'
        sys.exit(1)

    tra_ins = []
    tes_ins = []
    gkey_set = set([])
    tra_idx = 0
    all_cnt = 0

    # 1.Create two dictionaries, one using "user" as key and the other using "group" as key.
    ukey_item = {}
    gkey_item = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        all_cnt += 1
        if res[0] in ukey_item:
            ukey_item[res[0]].append(res[1])
        else:
            ukey_item[res[0]] = res[1:]
        if res[1] in gkey_item:
            gkey_item[res[1]].append(res[0])
        else:
            gkey_item[res[1]] = res[:1]

    # Sample accroding to the specified number
    if sys.argv[2].find('.') == -1:
        sample_cnt = int(sys.argv[2])
    # Sample accroding to the specified ratio
    else:
        ratio = float(sys.argv[2])
        sample_cnt = int(ceil(all_cnt*ratio))

    # 2.Loops over user keys and for each key, sample one group as training data. After finishing
    # this process, we can ensure every user id will occur in train data.
    for uid in ukey_item:
        gid = random.sample(ukey_item[uid], 1)
        ukey_item[uid].remove(gid[0])
        tra_ins.append([uid, gid[0]])
        gkey_set.add(gid[0])
        tra_idx += 1

    # 3.Check whether every group id occured in train data. For group id not occuring in train
    # data, sample one user as training data. After doing this, we can assure every group
    # id will occur in train data.
    for gid in gkey_item:
        if gid not in gkey_set:
            gkey_set.add(gid)
            uid = random.sample(gkey_item[gid], 1)
            ukey_item[uid[0]].remove(gid)
            tra_ins.append([uid[0], gid])
            tra_idx += 1

    # 4.For the left data, randomly partition them into train and test data accroding to the
    # specified ratio.
    left_dset = []
    for uid in ukey_item:
        for gid in ukey_item[uid]:
            left_dset.append([uid, gid])
    sample_ins = random.sample(left_dset, sample_cnt - tra_idx)
    tra_ins = tra_ins + sample_ins
    left_dset = map(lambda x: str(x[0])+'_'+str(x[1]), left_dset)
    sample_ins = map(lambda x: str(x[0])+'_'+str(x[1]), sample_ins)
    tes_ins = set(left_dset) - set(sample_ins)
    tes_ins = map(lambda x: [x.split('_')[0], x.split('_')[1]], tes_ins)

    # Output train and test segmentation result
    wfd = open(sys.argv[3], 'w')
    for tra in tra_ins:
        wfd.write("%s,%s\n" % (tra[0], tra[1]))
    wfd.close()
    wfd = open(sys.argv[4], 'w')
    for tes in tes_ins:
        wfd.write("%s,%s\n" % (tes[0], tes[1]))
    wfd.close()
