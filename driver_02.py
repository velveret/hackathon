# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 23:43:25 2012

@author: Rohan
"""

from node_02 import * 
from comp_coords_01 import *
from lagrange_01 import lagrange_01
from Physics_Calculator_02 import *

# Declare nodes
n1 = Segment(sp.Symbol('x_1'),sp.Symbol('y_1'),sp.Symbol('xd_1'),sp.Symbol('yd_1'),sp.Symbol('th_1'),sp.Symbol('thd_1'),"1", 1.0,1.0,0.5,1.0,True)
n2 = Mass(sp.Symbol('x_2'),sp.Symbol('y_2'),sp.Symbol('xd_2'),sp.Symbol('yd_2'),"2", 1.0,False)
n3 = Segment(sp.Symbol('x_3'),sp.Symbol('y_3'),sp.Symbol('xd_3'),sp.Symbol('yd_3'),sp.Symbol('th_3'),sp.Symbol('thd_3'),"3", 1.0,1.0,0.5,1.0,False)
n4 = Mass(sp.Symbol('x_4'),sp.Symbol('y_4'),sp.Symbol('xd_4'),sp.Symbol('yd_4'),"4", 1.0,False)
n5 = Segment(sp.Symbol('x_5'),sp.Symbol('y_5'),sp.Symbol('xd_5'),sp.Symbol('yd_5'),sp.Symbol('th_5'),sp.Symbol('thd_5'),"5", 1.0,1.0,0.5,1.0,False)
n6 = Mass(sp.Symbol('x_6'),sp.Symbol('y_6'),sp.Symbol('xd_6'),sp.Symbol('yd_6'),"6", 1.0,False)

#print "stuff"

# Organize nodes into a diagram
Diagram = {n1:[n2], n2:[n1, n3], n3:[n2, n4], n4:[n3,n5], n5:[n4,n6], n6:[n5]}

# Rewrite the coordinates of the nodes in terms of the 
# generalized coordinates
head = find_head(Diagram)
dfs(Diagram, head)

#print "*****************"
#print n2.xd
#print n2.yd
#print "*****************"
#print ""

#Compute the lagrangian
dgm = [n1, n2, n3, n4, n5, n6]
#print n1.x, "\n", n1.xd
L = sum([lagrange_01(n) for n in dgm])
L = sp.simplify(sp.expand(L))
print "\n\n\nL is \n", L, "\n\n\n"

# Compute and simulate differential equatoins
tAxis=np.linspace(0,50,10000)
(x,y,xdot,ydot)=sp.symbols(['th_1','th_2','thd_1','thd_2'])
EL = calcEL(L, [(x,xdot),(y,ydot)])
print "EL \n", EL, "\n\n\n"
F, out=numTimeEvolve(L,[(x,xdot),(y,ydot)],[(0,0),(3,0)],tAxis)
print F
