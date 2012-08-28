# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:22:17 2012

@author: Rohan
"""

import sympy  as sp

def convert_to_red(r, L):
    #Convert to redundant form
    th = sp.Symbol('th')
    thd= sp.Symbol('thd')
    x = r*L*sp.sin(th)
    y = r*L*sp.cos(th)
    xd= r*L*sp.cos(th)*thd
    yd=-r*L*sp.sin(th)*thd
    return (x,y,th,xd,yd,thd)
    
r = 2.0
L = 3.0
M = convert_to_red(r, L)
print M
