# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from sympy import *

class Node(object):
    __metaclass__ = ABCMeta
    objId = ""
    m = 0.0
    
    def __init__(self, newId, newM):
        self.objId, self.m = newId, newM
        self.x = Symbol("x_" + self.objId)
        self.y = Symbol("y_" + self.objId)
        self.xd = Symbol("xd_" +self. objId)
        self.yd = Symbol("yd_" + self.objId)
    @abstractmethod
    def __type__(self):
        pass
    def get_type(self):
        return self.__type__()

class Mass(Node):
    def __init__(self, newId, newM):
        super(Mass, self).__init__(newId, newM)
    def __type__(self):
        return "Mass"

class Segment(Node):
    I = 0.0
    r = 0.0
    L = 0.0
    
    def __init__(self, newId, newM, newI, newR, newL):
        super(Mass, self).__init__(newId, newM)
        self.I = newI
        self.r = newR
        self.L = newL
        self.th = Symbol("th" + self.objId)
        self.thd = Symbol("thd_" + self.objId)
        self.x0 = Symbol("x0_" + self.objId)
        self.y0 = Symbol("y0_" + self.objId)
        self.xf = Symbol("xf_" + self.objId)
        self.yf = Symbol("yf_" + self.objId)
    def __type__(self):
        return "Segment"

Node.register(Mass)
Node.register(Segment)