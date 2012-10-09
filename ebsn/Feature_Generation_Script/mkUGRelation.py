#!/usr/bin/env python
#encoding=utf8

'''
python mkUGRelation.py ../Clean_data/NewYork_user_group.csv ../Clean_data/NewYork_user_group.csv ../Temporal_Data/NewYork_user_group_sim.csv
'''

import sys

def calSim(user_groups, target_group, group_user_dic):
    source_users = set([])
    target_users = set([])

    for group in user_groups:
        if group != target_group:
            source_users |= set(group_user_dic[group])
        else:
            target_users |= set(group_user_dic[group])

    # user joined target group
    if len(target_users) > 0:
        comm = len(source_users&target_users)
        return [(comm-1)*1.0/(len(source_users|target_users)-1), comm]
    # user didn't join the target group
    else:
        target_users |= set(group_user_dic[target_group])
        comm = len(source_users&target_users)
        return [comm*1.0/(len(source_users|target_users)-1), comm]

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <user_group.in> <user_group_feature.in> <user_group_sim.out>'
        sys.exit(1)

    group_user_dic = {}
    user_group_dic = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if group_user_dic.has_key(res[1]):
            group_user_dic[res[1]].append(res[0])
        else:
            group_user_dic[res[1]] = [res[0]]
        if user_group_dic.has_key(res[0]):
            user_group_dic[res[0]].append(res[1])
        else:
            user_group_dic[res[0]] = [res[1]]

    wfd = open(sys.argv[3], 'w')
    for line in open(sys.argv[2]):
        res = line.strip('\n').split(',')
        [sim, comm]= calSim(user_group_dic[res[1]], res[2], group_user_dic)
        wfd.write("%s,%f,%d\n" % (line.strip('\n'), sim, comm))
    wfd.close()
