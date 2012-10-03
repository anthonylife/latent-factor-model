#!usr/bin/env python
#encoding=utf8

## Function: Analyse tags, including below method
#            1.get the number of tags which has text

import re
import sys

## Hyper parameter setting
preFreq = 5

def tagText(tagFile=None):
    if tagFile == None:
        tagFile = "../Meetup_tag/tag_text.csv"
    tagTextNum = 0
    p1 = re.compile(r'\W')
    p2 = re.compile(r'\w')
    targetFile1 = "../Meetup_tag/tag_long_text"
    targetFile2 = "../Meetup_tag/tag_short_text"
    targetFile3 = "../Meetup_tag/tag_short_sorted_text"
    targetFile4 = "../Meetup_tag/tag_text.new"

    wfd1 = open(targetFile1, 'w')
    wfd2 = open(targetFile2, 'w')
    wfd3 = open(targetFile3, 'w')
    wfd4 = open(targetFile4, 'w')

    all_text = []
    for line in open(tagFile):
        line = line.strip('\n')
        parts = line.split(',')
        if p2.findall(parts[1]):
            wfd4.write(line + '\n')
            tagTextNum += 1
            if p1.findall(parts[1]):
                wfd1.write(line + '\n')
            else:
                wfd2.write(line + '\n')
                all_text.append(parts)
    all_text.sort(key=lambda x: x[1])
    for text in all_text:
        wfd3.write(text[0] + ',' + text[1] + '\n')

    wfd1.close()
    wfd2.close()
    wfd3.close()
    wfd4.close()
    print tagTextNum

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



if __name__ == "__main__":
    #tagText()
    filterTags()
