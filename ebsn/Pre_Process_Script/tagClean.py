#!/usr/bin/env python
#encoding=utf8

## Function: Pre-processing tags
## Create Date: 2012/9/24

import sys

# Root path setting
dir_path = "../Meetup_tag/"

# Source file path setting
long_tag_file = "tag_long_text"
short_tag_file = "tag_short_text"
user_tag_file = "user_tag.csv"
group_tag_file = "group_tag.csv"

# Target file path setting
new_user_tag_file = "user_tag.new"
new_group_tag_file = "group_tag.new"
new_tag_text_file = "tag_text.new"

def loadShortTag(tag_id_dic = None, id_tag_dic = None):
    '''||--function only used here--||
        Discrip: Load short tag file and craete bi-directional dictionary
    '''
    if tag_id_dic == None:
        tag_id_dic = {}
    if id_tag_dic == None:
        id_tag_dic = {}

    for line in open(dir_path +  short_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        # Create bi-directional dictionary
        if not tag_id_dic.has_key(res[1]):
            tag_id_dic[res[1]] = res[0]
        if not id_tag_dic.has_key(res[0]):
            id_tag_dic[res[0]] = [res[1]]
    print len(tag_id_dic)
    return tag_id_dic, id_tag_dic


def loadLongTag(tag_id_dic = None, id_tag_dic = None):
    '''||--function only used here--||
        Discrip: Load long tag file and craete bi-directional dictionary
    '''
    if tag_id_dic == None:
        tag_id_dic = {}
    if id_tag_dic == None:
        id_tag_dic = {}

    for line in open(dir_path + long_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        tags = res[1].split('-')    # Segment the long tag

        # Create bi-directional dictionary
        for tag in tags:
            if not tag_id_dic.has_key(tag):
                tag_id_dic[tag] = res[0]
        if not id_tag_dic.has_key(res[0]):
            id_tag_dic[res[0]] = tags
    print len(tag_id_dic), len(id_tag_dic)
    '''Test '''
    '''cache_tag = {}
    count = 0
    for id in id_tag_dic.keys():
        for tag in id_tag_dic[id]:
            if not cache_tag.has_key(tag):
                count += 1
                cache_tag[tag] = 1
    print count'''

    return tag_id_dic, id_tag_dic

def getItemtag(id_tag_dic):
    '''||--function only used here--||
        Discription: Load user tagId relation and group tagId relation.
                    Then get their corresponding tags.
    '''
    user_tag_dic = {}
    group_tag_dic ={}

    # Load user tagid relation
    for line in open(dir_path + user_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if id_tag_dic.has_key(res[1]):
            tags = id_tag_dic[res[1]]
            if user_tag_dic.has_key(res[0]):
                user_tag_dic[res[0]] = list(set(user_tag_dic[res[0]]).union(set(tags)))     # Union set
            else:
                user_tag_dic[res[0]] = list(set(tags))

    # Load group tagid relation
    for line in open(dir_path + group_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if id_tag_dic.has_key(res[1]):
            tags = id_tag_dic[res[1]]
            if group_tag_dic.has_key(res[0]):
                group_tag_dic[res[0]] = list(set(group_tag_dic[res[0]]).union(set(tags)))     # Union set
            else:
                group_tag_dic[res[0]] = list(set(tags))

    ''' Test '''
    cache_tag = {}
    count = 0
    for user in user_tag_dic.keys():
        for tag in user_tag_dic[user]:
            if not cache_tag.has_key(tag):
                cache_tag[tag] = 1
                count += 1
    for group in group_tag_dic.keys():
        for tag in group_tag_dic[group]:
            if not cache_tag.has_key(tag):
                cache_tag[tag] = 1
                count += 1

    print count
    return user_tag_dic, group_tag_dic

def mkNewItemTagId(user_tag_dic, group_tag_dic, tag_id_dic):
    '''||--function only used here--||
        Discription: reorder the tags and then map user and tags accroding to new ids
    '''
    # tag id reorder
    wfd = open(dir_path + new_tag_text_file, 'w')
    for i,tag in enumerate(tag_id_dic.keys()):
        tag_id_dic[tag] = str(i + 1)
        wfd.write(tag_id_dic[tag] + ',' + tag + '\n')
    wfd.close()

    # get user's corresponding tag ids
    wfd = open(dir_path + new_user_tag_file, 'w')
    for user in user_tag_dic.keys():
        for tag in user_tag_dic[user]:
            if tag_id_dic.has_key(tag):
                wfd.write(user + ',' + tag_id_dic[tag] + '\n')
    wfd.close()

    # get group's corresponding tag ids
    wfd = open(dir_path + new_group_tag_file, 'w')
    for group in group_tag_dic.keys():
        for tag in group_tag_dic[group]:
            if tag_id_dic.has_key(tag):
                wfd.write(group + ',' + tag_id_dic[tag] + '\n')
    wfd.close()

def filterTags():
    '''Filter tags by the rules below:
        1.frequency
        2.stop words
        3.gini index
    '''
    user_tag_file = '../Meetup_tag/user_tag.new'
    group_tag_file = '../Meetup_tag/group_tag.new'
    tag_text_file = '../Meetup_tag/tag_text.new'
    tag_text_freq_file = "../Meetup_tag/tag_text_freq.sta"

    # Create tag text map
    tag_text_map = {}
    for line in open(tag_text_file):
        line = line.strip('\n')
        res = line.split(',')
        if tag_text_map.has_key(res[0]):
            print 'tag id key error.'
            sys.exit(1)

        tag_text_map[res[0]] = res[1]

    # create inverted index for tag, users and groups
    tag_item_map = {}
    for line in open(user_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if tag_text_map.has_key(res[1]):
            if tag_item_map.has_key(res[1]):
                tag_item_map[res[1]] += 1
            else:
                tag_item_map[res[1]] = 1

    for line in open(group_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if tag_text_map.has_key(res[1]):
            if tag_item_map.has_key(res[1]):
                tag_item_map[res[1]] += 1
            else:
                tag_item_map[res[1]] = 1

    # output tag and its corresponding frequency
    wfd = open(tag_text_freq_file, 'w')
    tag_item_map = tag_item_map.items()
    tag_item_map.sort(key = lambda x: x[1], reverse=True)

    tag_item_map = map(lambda x:str(x), tag_item_map)
    wfd.write('\n'.join(tag_item_map))
    wfd.close()

def checkTagNum():
    count = 0
    id_dic = {}
    word_dic = {}
    for line in open(dir_path + "tag_text.csv"):
        line = line.strip('\n')
        res = line.split(',')
        word_dic[res[0]] = 1

    for line in open(dir_path + user_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if not id_dic.has_key(res[1]):
            if word_dic.has_key(res[1]):
                count += 1
            id_dic[res[1]] = 0
    for line in open(dir_path + group_tag_file):
        line = line.strip('\n')
        res = line.split(',')
        if not id_dic.has_key(res[1]):
            if word_dic.has_key(res[1]):
                count += 1
            id_dic[res[1]] = 0
    print count


#=====================================
if __name__ == "__main__":

    print 'Start loading short tag...'
    [tag_id_dic, id_tag_dic] = loadShortTag()
    print 'Finish.'

    print 'Start loading long tag...'
    [tag_id_dic, id_tag_dic] = loadLongTag(tag_id_dic, id_tag_dic)
    print 'Finish.'

    print 'Start loading item tag...'
    [user_tag_dic, group_tag_dic] = getItemtag(id_tag_dic)
    print 'Finish.'

    print 'Start making new tag ids...'
    mkNewItemTagId(user_tag_dic, group_tag_dic, tag_id_dic)
    print 'Finish.'

    print 'Start to filter tags...'
    filterTags()
    print 'Finish.'
    #checkTagNum()
