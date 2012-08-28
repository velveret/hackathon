# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:35:50 2012

@author: Rohan
"""

import numpy  as np
import sympy  as sp
from node_02 import *

def lagrange_01(Seg):
    g = -10 
    
    # Checks the type
    if Seg.get_type() == "Mass":
        T = 1/2.0*Seg.m*Seg.xd**2 + 1/2.0*Seg.m*Seg.yd**2
        V = Seg.m*g*Seg.y
        L = T - V
    else:
        T = 1/2.0*Seg.m*Seg.xd**2 + 1/2.0*Seg.m*Seg.yd**2 + 1/2.0*Seg.I*Seg.thd**2
        V = Seg.m*g*Seg.y
        L = T - V
    #print L
    return L

#Seg = Segment("1",5.0, 1.0, 0.5, 1.0) # Mass("1",5.0) # 
#print Seg.m
#lagrange_01(Seg)
