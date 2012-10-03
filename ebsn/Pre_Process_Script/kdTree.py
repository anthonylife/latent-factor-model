#!/usr/bin/env python
#encoding=utf8

## For each user, get their events within certain specified distance.
## This script includes two main parts: 1.Create KDtree; 2.Search KDtree
## @date: 10/3/2012
## @author: anthonylife
## Sample excutable commander: python kdTree.py ../Clean_data/event_lon_lat.csv ../Clean_data/user_lon_lat.csv ../Clean_data/user_near_event.csv

import sys
from geopy import distance

## Global Variable Setting
# Number of dimensions
dimNum = 2
# Finish Points
totalFinishCnt = 0
#

# Create KD-tree
# ================
def createKDtree(input_file):
    '''# Test
    eventLocation = input_file'''

    eventLocation = {}
    for line in open(input_file):
        res = line.strip('\n').split(',')
        eventLocation[res[0]] = [float(res[1]), float(res[2])]

    kd_tree_root = {}
    tree_depth = 0
    iterCreateTree(kd_tree_root, tree_depth, eventLocation)
    return kd_tree_root

def iterCreateTree(root, treedep, leafset):
    '''
    Note: More than one point may have the same position.
    '''
    '''if not leafset:
        return treedep'''
    global totalFinishCnt
    left_son_tree = {}
    right_son_tree = {}
    # Dimension choice
    dim = treedep % dimNum
    median_num = median(map(lambda x: x[dim], leafset.values()))
    #print median_num
    for leaf in leafset.keys():
        if leafset[leaf][dim] < median_num:
            left_son_tree[leaf] = leafset[leaf]
        else:
            right_son_tree[leaf] = leafset[leaf]
        leafset.pop(leaf)

    #print left_son_tree
    #print right_son_tree
    # Iterative terminal condition
    if not left_son_tree:
        for key in right_son_tree.keys():
            root[key] = right_son_tree[key]
            totalFinishCnt += 1
        #print 'Finish Count: %d...' % totalFinishCnt
        '''print root
        raw_input()'''
        return True

    # Create sub-tree
    root[median_num] = [{}, {}]
    treedep += 1
    #print root[median_num][0]
    iterCreateTree(root[median_num][0], treedep, left_son_tree)
    #print root[median_num][0]
    '''print treedep
    raw_input()'''
    iterCreateTree(root[median_num][1], treedep, right_son_tree)


def median(numbers):
    '''Return the median of the list of numbers.'''
    # Sort the list of numbers and take the middle element.
    n = len(numbers)
    copy = numbers[:] # So that “numbers” keeps its original order
    copy.sort()
    if n & 1: # There is an odd number of elements
        return copy[n / 2]
    else:
        return (copy[n/2-1] + copy[n/2]) * 1.0 / 2

# Search KD-tree
# ==============
def searchKDtree(searchDataFile, outputFile):
    for line in open(searchDataFile):



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <event_location.in> <user_location.in> <user_event_near.out>'
        sys.exit(1)

    print "Start creating KD tree."
    kdTree = createKDtree(sys.argv[1])
    print "Finish creating KD tree."
    #searchKDtree(kdTree, sys.argv[2], sys.argv[3])

    '''# Test
    testEvent = {'1':[1,1], '2':[1,2], '3':[2,1], '4':[2,2]}
    kd_tree = createKDtree(testEvent)
    print kd_tree'''
