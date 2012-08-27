# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from sympy import *

class Node(object):
    __metaclass__ = ABCMeta
    x = Symbol('x')
    y = Symbol('y')
    xd = Symbol('xd')
    yd = Symbol('yd')
    m = 0.0
    
    def __init__(self, newM):
        self.m = newM
    @abstractmethod
    def __type__(self):
        pass
    def get_type(self):
        return self.__type__()

class Mass(Node):
    def __init__(self, newM):
        super(Mass, self).__init__(newM)
    def __type__(self):
        return "Mass"

class Segment(Node):
    th = 0.0
    thd = Symbol('thd')
    x0 = Symbol('x0')
    y0 = Symbol('y0')
    xf = Symbol('xf')
    yf = Symbol('yf')
    I = 0.0
    r = 0.0
    L = 0.0
    
    def __init__(self, newM, newTh, newI, newR, newL):
        super(Mass, self).__init__(newM)
        self.th = newTh
        self.I = newI
        self.r = newR
        self.L = newL
    def __type__(self):
        return "Segment"

Node.register(Mass)
Node.register(Segment)