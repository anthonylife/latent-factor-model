#!/usr/bin/env python
#encoding=utf8

## For each user, get their events within certain specified distance.
## This script includes two main parts: 1.Create KDtree; 2.Search KDtree
## @date: 10/3/2012
## @author: anthonylife
## Sample excutable commander: python kdTree.py ../Clean_data/event_lon_lat.csv ../Clean_data/user_lon_lat.csv ../Clean_data/user_near_event.csv

import sys
#import math
import datetime
from geopy import distance

## Global Variable Setting
# Number of dimensions
dimNum = 2
# Finish Points
totalFinishCnt = 0
# Distance threshold
mileThreshold = 20

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
    global totalFinishCnt
    left_son_tree = {}
    right_son_tree = {}
    # Dimension choice
    dim = treedep % dimNum
    median_num = median(map(lambda x: x[dim], leafset.values()))
    for leaf in leafset.keys():
        if leafset[leaf][dim] < median_num:
            left_son_tree[leaf] = leafset[leaf]
        else:
            right_son_tree[leaf] = leafset[leaf]
        leafset.pop(leaf)

    # Iterative terminal condition
    if not left_son_tree:
        for key in right_son_tree.keys():
            root[key] = right_son_tree[key]
            totalFinishCnt += 1
        #print 'Finish Count: %d...' % totalFinishCnt
        return True

    # Create sub-tree
    root[median_num] = [{}, {}]
    treedep += 1
    iterCreateTree(root[median_num][0], treedep, left_son_tree)
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
def searchKDtree(kdTree, searchDataFile, outputFile):
    wfd = open(outputFile, 'w')
    user_cnt = 0
    begin_time = datetime.datetime.now()
    for line in open(searchDataFile):
        res = line.strip('\n').split(',')
        user_id = res[0]
        location_val = map(lambda x: float(x), res[1:])

        # Find the nearest negibhor and get search path
        depth = 0
        search_path = []
        near_events = []
        searchNearestNeighbor(location_val, kdTree, search_path, depth, near_events)

        # Get the list of events which meets the distance requirement
        backSearchTree(location_val, search_path, near_events)
        #print user_id
        #print near_events
        #raw_input()
        for event_id in near_events:
            wfd.write("%s,%s\n" % (user_id, event_id))
        '''# Test
        wfd.close()
        return'''
        user_cnt +=1
        if user_cnt % 2 == 0:
            end_time = datetime.datetime.now()
            print 'Cnt: %d, Cost time: %d...' % (user_cnt, (end_time-begin_time).seconds)
            begin_time = datetime.datetime.now()
    wfd.close()

    '''# Test
    user_id = 123
    location_val = [1.1, 1.1]
    # Find the nearest negibhor and get search path
    depth = 0
    search_path = []
    near_events = []
    searchNearestNeighbor(location_val, kdTree, search_path, depth, near_events)
    print search_path
    # Get the list of events which meets the distance requirement
    backSearchTree(location_val, search_path, near_events)
    print 'Final result...'
    print near_events'''

def searchNearestNeighbor(locationVal, kdTree, searchPath, depth, nearEvents):
    dim = depth%dimNum
    #print kdTree
    key = kdTree.keys()
    # Terminal Condition --> reach the leaf
    #print type(kdTree[key[0]][0])
    if type(kdTree[key[0]][0]) == type(0) or type(kdTree[key[0]][0]) == type(0.0):
        for key in kdTree.keys():
            if distance.distance([locationVal[1], locationVal[0]], [kdTree[key][1], kdTree[key][0]]).miles <= mileThreshold:
                nearEvents.append(key)
            '''# Test
            if math.sqrt((locationVal[0]-kdTree[key][0])**2 + (locationVal[1]-kdTree[key][1])**2) <= mileThreshold:
                nearEvents.append(key)'''
        return

    # Tree's interior node should meet the tree structure
    if len(key) != 1:
        print 'Not tree structure.'
        sys.exit(1)

    key = key[0]
    # Iterative Search
    depth += 1
    if locationVal[dim] < key:
        searchPath.append(kdTree[key][1])  # Note: store the reverse search direction of point.
        searchNearestNeighbor(locationVal, kdTree[key][0], searchPath, depth, nearEvents)
    else:
        searchPath.append(kdTree[key][0])
        searchNearestNeighbor(locationVal, kdTree[key][1], searchPath, depth, nearEvents)

def backSearchTree(locationVal, searchPath, nearEvents):
    dep_cnt = 0
    for root in reversed(searchPath):
        dep_cnt += 1
        if not traverseTree(root, locationVal, nearEvents):
            print 'Dep count: %d...' % dep_cnt
            return

def traverseTree(root, locationVal, nearEvents):
    '''
    Binary tree traversal
    '''
    key = root.keys()
    # Terminal Condition --> reach the leaf
    tag = False
    if type(root[key[0]][0]) == type(0) or type(root[key[0]][0]) == type(0.0):
        for key in root.keys():
            if distance.distance([locationVal[1], locationVal[0]], [root[key][1], root[key][0]]).miles <= mileThreshold:
                nearEvents.append(key)
                tag = True
            '''# Test
            if math.sqrt((locationVal[0]-root[key][0])**2 + (locationVal[1]-root[key][1])**2) <= mileThreshold:
                nearEvents.append(key)
                tag = True'''
        return tag

    if len(key) != 1:
        print 'Not tree structure.'
        sys.exit(1)

    key = root.keys()[0]
    tag_left = traverseTree(root[key][0], locationVal, nearEvents)
    tag_right = traverseTree(root[key][1], locationVal, nearEvents)
    if tag_left or tag_right:
        return True
    return False

# Main function
# =============
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <event_location.in> <user_location.in> <user_event_near.out>'
        sys.exit(1)

    print "Start creating KD tree."
    kd_tree = createKDtree(sys.argv[1])
    print "Finish creating KD tree."
    searchKDtree(kd_tree, sys.argv[2], sys.argv[3])

    '''# Test
    testEvent = {'1':[1,1], '2':[1,2], '3':[2,1], '4':[2,2]}
    kd_tree = createKDtree(testEvent)
    print kd_tree
    searchKDtree(kd_tree, 'sadf', 'sdf')'''

