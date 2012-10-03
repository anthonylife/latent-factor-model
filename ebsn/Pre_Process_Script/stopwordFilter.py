#!/usr/bin/env python
#encoding=utf8

# Count the stop words in tag list and filter them
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'Useage: <stopword.dic> <tag.text>'

    stopword = {}
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        stopword[line] = 1

    totalCnt = 0
    nonStopCnt = 0
    for line in open(sys.argv[2]):
        totalCnt += 1
        word = line.strip('\n').split(',')[1]
        if not stopword.has_key(word):
            nonStopCnt += 1

    print 'Total word count: %d...' % totalCnt
    print 'Non stopword count: %d...' % nonStopCnt

    # Get the freq of tags belonging to stopwords

