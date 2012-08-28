# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 19:10:13 2012

@author: Rohan
"""

# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from sympy import *

class Node(object):
    __metaclass__ = ABCMeta
    m = 0.0
    fixed = False
    
    def __init__(self, xSym, ySym, xdSym, ydSym, newM, isFixed):
        self.m = newM
        self.x = xSym # Symbol("x_" + self.objId)
        self.y = ySym # Symbol("y_" + self.objId)
        self.xd= xdSym # Symbol("xd_" +self. objId)
        self.yd= ydSym # Symbol("yd_" + self.objId)
        self.fixed = isFixed
    @abstractmethod
    def __type__(self):
        pass
    def get_type(self):
        return self.__type__()

class Mass(Node):
    def __init__(self, xSym, ySym, xdSym, ydSym, newM, isFixed):
        super(Mass, self).__init__(xSym, ySym, xdSym, ydSym, newM, isFixed)
    def __type__(self):
        return "Mass"

class Segment(Node):
    I = 0.0
    r = 0.0
    L = 0.0
    
    def __init__(self, xSym, ySym, xdSym, ydSym, thSym, thdSym, newM, newI, newR, newL, isFixed):
        super(Segment, self).__init__(xSym, ySym, xdSym, ydSym, newM, isFixed)
        self.I = newI
        self.r = newR
        self.L = newL
        self.th = thSym # Symbol("th" + self.objId)
        self.thd = thdSym # Symbol("thd_" + self.objId)
#        self.x0 = Symbol("x0_" + self.objId)
#        self.y0 = Symbol("y0_" + self.objId)
#        self.xf = Symbol("xf_" + self.objId)
#        self.yf = Symbol("yf_" + self.objId)
    def __type__(self):
        return "Segment"

Node.register(Mass)
Node.register(Segment)