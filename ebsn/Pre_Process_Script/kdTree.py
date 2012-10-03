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
def searchKDtree(kdTree, searchDataFile, outputFile):
    wfd = open(outputFile, 'w')
    for line in open(searchDataFile):
        res = line.split(',')
        user_id = res[0]
        location_val = map(lambda x: float(x), res[1:])

        # Find the nearest negibhor and get search path
        depth = 0
        search_path = []
        near_events = []
        searchNearestNeighbor(location_val, kdTree, search_path, depth, near_events)

        # Get the list of events which meets the distance requirement
        backSearchTree(location_val, search_path, near_events)
        print user_id
        print near_events
        raw_input()
        for event_id in near_events:
            wfd.write("%s,%s\n" % (user_id, event_id))
    wfd.close()

def searchNearestNeighbor(locationVal, kdTree, searchPath, depth, near_events):
    dim = depth%dimNum
    key = kdTree.keys()
    # Terminal Condition --> reach the leaf
    if type(kdTree[key][0]) == 'int' or type(kdTree[key][0]) == 'float':
        for key in kdTree.keys():
            if distance.distance(locationVal, kdTree[key]).miles <= mileThreshold:
                near_events.append(key)
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
        searchNearestNeighbor(locatioinVal, kdTree[key][0], searchPath, depth)
    else:
        searchPath.append(kdTree[key][0])
        searchNearestNeighbor(locatioinVal, kdTree[key][1], searchPath, depth)

def backSearchTree(locationVal, searchPath, near_events):
    for root in reversed(searchPath):
        if traverseTree(root, locationVal, near_events):
            return

def traverseTree(root, locationVal, near_events):
    '''
    Binary tree traversal
    '''


# Main function
# =============
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'usage: <event_location.in> <user_location.in> <user_event_near.out>'
        sys.exit(1)

    print "Start creating KD tree."
    kd_tree = createKDtree(sys.argv[1])
    print "Finish creating KD tree."
    searchKDtree(kdTree, sys.argv[2], sys.argv[3])

    '''# Test
    testEvent = {'1':[1,1], '2':[1,2], '3':[2,1], '4':[2,2]}
    kd_tree = createKDtree(testEvent)
    print kd_tree'''
