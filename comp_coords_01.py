# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 18:42:43 2012

@author: Rohan
"""

from node_02 import *

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
    diagramCopy = copy.deepCopy(diagram)
    for node in visited:
        del diagramCopy[node]
    return find_head(diagramCopy)

def dfs(diagram, head):
    visited = []
    parents = {}
    next = []
    next.append(head)
    parents[head] = None
    while len(visited) < len(diagram.keys()):
        if len(next) == 0:
            next.append(get_unvisited(diagram, visited))
            parents[head] = None
            continue
        else:
            current = next.pop()
            visited.append(current)
            print "visiting %s with parent %s" % (current.x,\
                parents[current].x if parents[current] else None)
            for child in diagram[current]:
                if not (child in visited or child in next):
                    next.append(child)
                    parents[child] = current
    return parents
                
n1 = Mass('x_1','y_1','xd_1','yd_1',"1",1.0,False)
n2 = Segment('x_2','y_2','xd_2','yd_2','th_2','thd_2',"2", 2.0,1.0,0.5,1.0,True)
n3 = Segment('x_3','y_3','xd_3','yd_3','th_3','thd_3',"3", 2.0,1.0,0.5,1.0,False)

Diagram = {n1:[n2, n3], n2:[n1], n3:[n1]}
head = find_head(Diagram)
print dfs(Diagram, head)