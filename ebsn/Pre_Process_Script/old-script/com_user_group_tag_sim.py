#!/usr/bin/env python
#encoding=utf8

## Function: Three main task:1.Compute the tags' similarity between user and user, user and group, group and group.
#  Create: 2012/9/21
# Last Modified:

## Global Variable Setting
# File Path
Group_tag_file = "../Meetup_tag/group_tag.csv"
User_tag_file = "../Meetup_tag/user_tag.csv"
Group_user_file = "../Sta_Data/group_has_user.dat"

def loadInfo():
    ''' Function: Load group tags' information and user tags' information
                    Store in dictionary.
    '''
    group_tag = {}
    for line in open(Group_tag_file):
        line = line.strip('\n')
        arr = line.split(',')
        if group_tag.has_key(arr[0]):
            group_tag[arr[0]] = group_tag[arr[0]] + [arr[1]]
        else:
            group_tag[arr[0]] = [arr[1]]
    print 'finish 1'
    user_tag = {}
    for line in open(User_tag_file):
        line = line.strip('\n')
        arr = line.split(',')
        if user_tag.has_key(arr[0]):
            user_tag[arr[0]] = user_tag[arr[0]] + [arr[1]]
        else:
            user_tag[arr[0]] = [arr[1]]

    print 'finish 2'
    return [group_tag, user_tag]

def calSim(group_tags, user_tags):
    ''' Function: calculate the number of common tags and pearson coefficient between groups and tags
    '''
    #group_tags = [12,3,4]
    #user_tags = [3,4,9]
    print group_tags
    print user_tags
    com = len(set(group_tags) & set(user_tags))
    union = len(set(group_tags) | set(user_tags))

    return [com, com/1.0/union]


if __name__ == "__main__":

    # Load tag resources, relation information of users belonging to groups
    [group_tag, user_tag] = loadInfo()

    # Calculate similarity of tags between users and tags
    #group_tag = {}
    #user_tag = {}
    cache_group_id = 0
    for line in open(Group_user_file):
        line = line.strip('\n')
        arr = line.split(',')
        #if cache_group_id != arr[1]:
        #    cache_group_id = arr[1]
        if group_tag.has_key(arr[1]) and user_tag.has_key(arr[0]):
            [com, pearson] = calSim(group_tag[arr[1]], user_tag[arr[0]])
        #[com, pearson] = calSim(group_tag, user_tag)
            print "%d, %f" % (com, pearson)
            raw_input('pause')
