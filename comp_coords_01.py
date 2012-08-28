# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 18:42:43 2012

@author: Rohan
"""

from node_02 import *
import sympy as sp
import copy

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
    diagramCopy = copy.copy(diagram)
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
            newHead = get_unvisited(diagram, visited)
            next.append(newHead)
            parents[newHead] = None
            continue
        else:
            current = next.pop()
            visited.append(current)
#            print "visiting %s with parent %s" % (current.objId,\
#                parents[current].objId if parents[current] else None)
            
            # Calculate qualities
            if parents[current]:
                if current.get_type() == "Segment" and parents[current].get_type() == "Segment" :
                    current.x0= parents[current].xf
                    current.y0= parents[current].yf
                    current.xf= current.x0 + current.L*sp.cos(current.th)
                    current.yf= current.y0 + current.L*sp.sin(current.th)
                    current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                    current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                    current.xd= parents[current].xd - parents[current].L*sp.sin(parents[current].th)*parents[current].thd - current.r*current.L*sp.sin(current.th) * current.thd
                    current.yd= parents[current].yd + parents[current].L*sp.cos(parents[current].th)*parents[current].thd + current.r*current.L*sp.cos(current.th) * current.thd
                elif current.get_type() == "Segment" and parents[current].get_type() == "Mass" :
                    current.x0= parents[current].x
                    current.y0= parents[current].y
                    current.xf= current.x0 + current.L*sp.cos(current.th)
                    current.yf= current.y0 + current.L*sp.sin(current.th)
                    current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                    current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                    current.xd= parents[current].xd - current.r*current.L*sp.sin(current.th) * current.thd
                    current.yd= parents[current].yd + current.r*current.L*sp.cos(current.th) * current.thd
                else: #  current.get_type() == "Mass" and parents[current].get_type() == "Segment" :
                    current.x = parents[current].xf
                    current.y = parents[current].yf
                    current.xd= parents[current].xd - parents[current].L*sp.sin(parents[current].th)*parents[current].thd
                    current.yd= parents[current].yd + parents[current].L*sp.cos(parents[current].th)*parents[current].thd                    
            else:
                if current.fixed:
                    current.x0= 0.0
                    current.y0= 0.0
                else:
                    print "CHECK ", current.x0
                current.xf= current.x0 + current.L*sp.cos(current.th)
                current.yf= current.y0 + current.L*sp.sin(current.th)
                current.x = current.x0 + current.r*current.L*sp.cos(current.th)
                current.y = current.y0 + current.r*current.L*sp.sin(current.th)
                current.xd= - current.r*current.L*sp.sin(current.th) * current.thd
                current.yd=   current.r*current.L*sp.cos(current.th) * current.thd
#            print current.objId
#            print current.x
#            print current.y
#            print "" 
            
            for child in diagram[current]:
                if not (child in visited or child in next):
                    next.append(child)
                    parents[child] = current
    return parents
                
#n1 = Mass(sp.Symbol('x_1'),sp.Symbol('y_1'),sp.Symbol('xd_1'),sp.Symbol('yd_1'),"1",1.0,False)
#n2 = Segment(sp.Symbol('x_2'),sp.Symbol('y_2'),sp.Symbol('xd_2'),sp.Symbol('yd_2'),sp.Symbol('th_2'),sp.Symbol('thd_2'),"2", 2.0,1.0,0.5,1.0,True)
#n3 = Segment(sp.Symbol('x_3'),sp.Symbol('y_3'),sp.Symbol('xd_3'),sp.Symbol('yd_3'),sp.Symbol('th_3'),sp.Symbol('thd_3'),"3", 2.0,1.0,0.5,1.0,False)
#
#Diagram = {n1:[n2, n3], n2:[n1], n3:[n1]}
#head = find_head(Diagram)
#print dfs(Diagram, head)