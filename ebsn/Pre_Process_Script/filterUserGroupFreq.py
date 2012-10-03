#!/usr/bin/env python
#encoding=utf8

'''
python filterUserGroupFreq.py ../Temporal_Data/user_group.temp.1 ../Temporal_Data/user.temp.1 ../Temporal_Data/group.temp.1
'''

import sys

# Filter condition: 1.user should have attended at least 5 groups, 2.group should have at least 5 people
freq_threshold_user = 5
freq_threshold_group = 5

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <user_group.in> <user.out> <group.out>'
        sys.exit(1)

    user_group_nums = {}
    group_user_nums = {}
    for line in open(sys.argv[1]):
        res = line.strip('\n').split(',')
        if user_group_nums.has_key(res[0]):
            user_group_nums[res[0]] += res[1:]
        else:
            user_group_nums[res[0]] = res[1:]

        if group_user_nums.has_key(res[1]):
            group_user_nums[res[1]] += res[:1]
        else:
            group_user_nums[res[1]] = res[:1]
    print 'Finish loading user_group.info'

    conv = False
    user_has_group = 0
    group_has_user = 0
    loop_cnt = 0
    print_interval = 2
    while not conv:
        for user in user_group_nums.keys():
            if len(user_group_nums[user]) < freq_threshold_user:
                for group in user_group_nums[user]:
                    group_user_nums[group].remove(user)
                user_group_nums.pop(user)
                #print user
        temp_user = len(map(lambda x: len(x[1]), user_group_nums.items()))

        for group in group_user_nums.keys():
            if len(group_user_nums[group]) < freq_threshold_group:
                for user in group_user_nums[group]:
                    user_group_nums[user].remove(group)
                group_user_nums.pop(group)
                #print group
        temp_group = len(map(lambda x: len(x[1]), group_user_nums.items()))

        if temp_user == user_has_group and temp_group == group_has_user:
            conv = True
        else:
            user_has_group = temp_user
            group_has_user = temp_group

        loop_cnt += 1
        if loop_cnt % print_interval == 0:
            print 'Loops: %d, User have groups: %d, Group have users: %d.' % (loop_cnt, user_has_group, group_has_user)

    wfd = open(sys.argv[2], 'w')
    for user in user_group_nums.keys():
        wfd.write(user + '\n')
    wfd.close()

    wfd = open(sys.argv[3], 'w')
    for group in group_user_nums.keys():
        wfd.write(group + '\n')
    wfd.close()
