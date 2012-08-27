# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 18:42:43 2012

@author: Rohan
"""

# Given dictionary (graph), compute coordinates of nodes
def comp_coords_01(diagram, nodeSet):
    # diagram: dictionary showing elements and connectivity
    # nodeSet: set of Nodes in the diagram
    
    while len(nodeSet) > 0:
        # Find a "fixed" node that is still in set
        