# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 18:42:43 2012

@author: Rohan
"""

from node_02 import *
from sets import Set

# Given dictionary (graph), compute coordinates of nodes
#def comp_coords_01(diagram, nodeSet):
    # diagram: dictionary showing elements and connectivity
    # nodeSet: set of Nodes in the diagram

def find_head(diagram):
    for node in diagram.keys():
        if node.fixed:
            return node
    return diagram.keys()[0]

def get_unvisited(diagram, visited):
    visitedSet = Set(visited)
    nodeSet = Set(diagram.keys())
    unvisited = nodeSet.difference(visitedSet)
    return unvisited.pop()

def dfs(diagram, head):
    visited = []
    next = []
    next.append(head)
    prev = None
    while len(visited) < len(diagram.keys()):
        if len(next) == 0:
            next.append(get_unvisited(diagram, visited))
            prev = None
            continue
        else:
            current = next.pop()
            visited.append(current)
            print "visiting %s with previous %s" % (current.x, prev.x if prev else None)
            if not current.fixed:
                # process here
                print "processing"
                
            for child in diagram[current]:
                if not (child in visited or child in next):
                    next.append(child)
            prev = current

                
n1 = Mass('x_1','y_1','xd_1','yd_1',1.0,False)
n2 = Segment('x_2','y_2','xd_2','yd_2','th_2','thd_2',2.0,1.0,0.5,1.0,True)
n3 = Segment('x_3','y_3','xd_3','yd_3','th_3','thd_3',2.0,1.0,0.5,1.0,False)

Diagram = {n1:[n2, n3], n2:[n1], n3:[n1]}
head = find_head(Diagram)
dfs(Diagram, head)