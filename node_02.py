# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 19:10:13 2012

@author: Rohan
"""

# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
import sympy as sp

class Node(object):
    __metaclass__ = ABCMeta
    objId = ""
    m = 0.0
    fixed = False
    
    def __init__(self, xSym, ySym, xdSym, ydSym, newId, newM, isFixed):
        self.m = newM
        self.objId = newId
        self.x = xSym
        self.y = ySym
        self.xd= xdSym
        self.yd= ydSym
        self.fixed = isFixed
    @abstractmethod
    def __type__(self):
        pass
    def get_type(self):
        return self.__type__()

class Mass(Node):
    def __init__(self, xSym, ySym, xdSym, ydSym, newId, newM, isFixed):
        super(Mass, self).__init__(xSym, ySym, xdSym, ydSym, newId, newM,\
            isFixed)
    def __type__(self):
        return "Mass"

class Segment(Node):
    I = 0.0
    r = 0.0
    L = 0.0
    x0 = 0.0
    y0 = 0.0
    xf = 0.0
    yf = 0.0
    
    def __init__(self, xSym, ySym, xdSym, ydSym, thSym, thdSym, newId, newM,\
            newI, newR, newL, isFixed):
        super(Segment, self).__init__(xSym, ySym, xdSym, ydSym, newId, newM,\
            isFixed)
        self.I = newI
        self.r = newR
        self.L = newL
        self.th = thSym
        self.thd = thdSym
        self.x0 = self.x + self.r*self.L* sp.cos(self.th)
        self.y0 = self.y + self.r*self.L* sp.sin(self.th)
        self.xf = self.x - (1-self.r)*self.L*sp.cos(self.th)
        self.yf = self.y - (1-self.r)*self.L*sp.sin(self.th)
    def __type__(self):
        return "Segment"

Node.register(Mass)
Node.register(Segment)