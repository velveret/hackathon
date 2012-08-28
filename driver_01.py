# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 23:43:25 2012

@author: Rohan
"""

from node_02 import * 
from comp_coords_01 import *
from lagrange_01 import lagrange_01
from Physics_Calculator import *

# Declare nodes
n1 = Segment(sp.Symbol('x_1'),sp.Symbol('y_1'),sp.Symbol('xd_1'),sp.Symbol('yd_1'),sp.Symbol('th_1'),sp.Symbol('thd_1'),"1", 1.0,1.0,0.5,1.0,True)
n2 = Segment(sp.Symbol('x_2'),sp.Symbol('y_2'),sp.Symbol('xd_2'),sp.Symbol('yd_2'),sp.Symbol('th_2'),sp.Symbol('thd_2'),"2", 1.0,1.0,0.5,1.0,False)

# Organize nodes into a diagram
Diagram = {n1:[n2], n2:[n1]}

# Rewrite the coordinates of the nodes in terms of the 
# generalized coordinates
head = find_head(Diagram)
dfs(Diagram, head)

print "*****************"
print n2.y
print n2.yd
print "*****************"
print ""

#Compute the lagrangian
dgm = [n1, n2]
print n1.x, "\n", n1.xd
L = sum([lagrange_01(n) for n in dgm])
L = sp.simplify(sp.expand(L))
print "\n\n\nL is \n", L, "\n\n\n"

# Compute and simulate differential equatoins
#tAxis=np.linspace(0,50,10000)
#(x,y,xdot,ydot)=sp.symbols(['th_1','th_2','thd_1','thd_2'])
#EL = calcEL(L, [(x,xdot),(y,ydot)])
#print EL
#out=numTimeEvolve(L,[(x,xdot),(y,ydot),(lam,lamdot)],[(0,0),(3,0)],tAxis)
