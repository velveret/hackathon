# -*- coding: utf-8 -*-
from abc import abstractmethod
from abc import ABCMeta
import pygame as pg
import numpy as np
from math import atan2,sin,cos
from node_02 import Mass
from sympy import Symbol
import node_02
import copy

blackColor = pg.Color(0, 0, 0)
blueColor = pg.Color(0, 0, 255)
whiteColor = pg.Color(255, 255, 255)
currentId = 0

class StaticDrawing():
    @staticmethod
    def pointIntersect(x0, y0, x1, y1):
        return x0 == x1 and y0 == y1
    # assumes points aren't on top of each other/same for segments
    @staticmethod
    def intersects(obj1, obj2):
        if obj1.get_type() == "Point" and obj2.get_type() == "Segment":
            return StaticDrawing.pointIntersect(obj1.x, obj1.y, obj2.x0, obj2.y0) or\
                StaticDrawing.pointIntersect(obj1.x, obj1.y, obj2.x1, obj2.y1)
        elif obj2.get_type() == "Point" and obj1.get_type() == "Segment":
            return StaticDrawing.pointIntersect(obj2.x, obj2.y, obj1.x0, obj1.y0) or\
                StaticDrawing.pointIntersect(obj2.x, obj2.y, obj1.x1, obj1.y1)
        else:
            return False
    @staticmethod
    def makeDiagram(drawables, origin):
        drawingToNode = {}
        diagram = {}
        varList = []
        angleDict = {}
        for obj in drawables:
            node, newVars = obj.translate(origin)
            varList.extend(newVars)
            if obj.get_type() == "Segment":
                angleDict[node.th] = obj.getTheta()
            drawingToNode[obj] = node
            diagram[node] = set()
        unvisited = copy.copy(drawables)
        for obj in drawables:
            for obj2 in unvisited:
                if StaticDrawing.intersects(obj, obj2):
                    diagram[drawingToNode[obj]].add(drawingToNode[obj2])
                    diagram[drawingToNode[obj2]].add(drawingToNode[obj])
            unvisited.remove(obj)
        return diagram, varList, angleDict

class Drawable(object):
    __metaclass__ = ABCMeta
    x = 0.0
    y = 0.0
    m = 0.0
    fixed = False
    def __init__(self, newSurface, newX, newY, newM, isFixed):
        self.x = newX
        self.y = newY
        self.surface = newSurface
        self.m = newM
        self.fixed = isFixed
        global currentId
        self.objId = str(currentId)
        currentId = currentId + 1
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def get_type(self):
        pass
    def setX(self, newX):
        self.x = newX
    def setY(self, newY):
        self.y = newY
    def setMass(self, newM):
        self.m = newM
    def setFixed(self, isFixed):
        self.fixed = isFixed
    @abstractmethod
    def translate(self, origin):
        pass
    def makeSym(self,prefix=""):
        return Symbol(prefix + "_" + self.objId)

# parameters:
# surface: to be drawn on
# x: x-coordinate of center relative to surface
# y: y-coordinate center relative to surface
# optional params:
# m: mass (default is 1.0)
# fixed: whether it is fixed (default is False)
# r: radius of point to the drawn (default is 5)
class Point(Drawable):
    r = 0.0
    def __init__(self, surface, newX, newY, newM=1.0, isFixed=False, newR=10):
        super(Point, self).__init__(surface, newX, newY, newM, isFixed)
        self.r = newR
#        self.isFixed = isFixed
    def draw(self):
        if self.fixed:
            pg.draw.circle(self.surface, blackColor, (self.x, self.y), self.r)
            pg.draw.line(self.surface, (255,0,0), (self.x-self.r, self.y), (self.x+self.r, self.y), 3)
            pg.draw.line(self.surface, (255,0,0), (self.x, self.y-self.r), (self.x, self.y+self.r), 3)
        else:
            pg.draw.circle(self.surface, blackColor, (self.x, self.y), self.r)
    def get_type(self):
        return "Point"
    def setR(self, newR):
        self.r = newR
    def translate(self, origin):
        if self.fixed:
            return Mass(self.x-origin[0], self.y-origin[1], 0, 0,self.objId, self.m, self.fixed), []
        else:
            node = Mass(self.makeSym("x"), self.makeSym("y"), self.makeSym("xd"),\
            self.makeSym("yd"),self.objId, self.m, self.fixed)
            return node, [(node.x, node.xd), (node.y, node.yd)]

# parameters:
# surface: to be drawn on
# x0,y0: coordinate of first endpoint
# x1,y1: coordinate of second endpoint
# optional params:
# I: moment of inertia (default is 1.0)
# r: ratio representing distance from centroid, ranges from 0.0 to 1.0
#    (default is 0.5)
# m: mass (default is 1.0)
# fixed: whether it is fixed (default is False)
class Segment(Drawable):
    x1 = 0.0
    y1 = 0.0
    def __init__(self, surface, x0, y0, newX1, newY1, newI=1.0, newR=0.5,\
            newM=1.0, isFixed=False):
        super(Segment, self).__init__(surface, x0, y0, newM, isFixed)
        self.x0 = x0
        self.y0 = y0
        self.x1 = newX1
        self.y1 = newY1
        self.I = newI
        self.r = Segment.maybeValidRatio(newR)
    def draw(self):
        pg.draw.line(self.surface, blueColor, (self.x0, self.y0), (self.x1,\
            self.y1), 5)
    def get_type(self):
        return "Segment"    
    def getLength(self):
        return np.sqrt((self.x0-self.x1)**2 + (self.y0-self.y1)**2)
    # set switch to True to use (x1,y1) as the reference point to be shifted
    # to the origin
    # returns angle relative to (0,0)->(0,-pi/2) 
    def getTheta(self, switch=False):
        if switch:
            newX = self.x0 - self.x1
            newY = self.y0 - self.y1
            return atan2(newX, newY)-np.pi/2.0
        else:
            newX = self.x1 - self.x0
            newY = self.y1 - self.y0
            return atan2(newX, newY)-np.pi/2.0
    def setX0(self, newX):
        self.x0 = newX
    def setX1(self, newX):
        self.x1 = newX
    def setY0(self, newY):
        self.y0 = newY
    def setY1(self, newY):
        self.y1 = newY
    def setMomentOfInertia(self, newI):
        self.I = newI
    def setRatioDistanceToCentroid(self, newR):
        try:        
            self.r = Segment.maybeValidRatio(newR)
        except AttributeError:
            pass
    # set switch to True to use (x1,y1) as the fixed point
    def setLength(self, length, switch=False):
        ratio = self.getLength() / float(length)
        if switch:
            self.setX0(self.x1 + (self.x0 - self.x1) / ratio)
            self.setY0(self.y1 + (self.y0 - self.y1) / ratio)
        else:
            self.setX1(self.x0 + (self.x1 - self.x0) / ratio)
            self.setY1(self.y0 + (self.y1 - self.y0) / ratio)
    # set switch to True to use (x1,y1) as the fixed point 
    # theta should be in radians
    def rotate(self, theta, switch=False):
        if switch:
            newX = self.x0 - self.x1
            newY = self.y0 - self.y1  
            newX, newY = newX * cos(theta) - newY * sin(theta) + self.x1,\
                newX * sin(theta) + newY * cos(theta) + self.y1
            self.setX0(newX)
            self.setY0(newY)
        else:
            newX = self.x1 - self.x0
            newY = self.y1 - self.y0  
            newX, newY = newX * cos(theta) - newY * sin(theta) + self.x0,\
                newX * sin(theta) + newY * cos(theta) + self.y0
            self.setX1(newX)
            self.setY1(newY)
    def translate(self, origin):
        node = node_02.Segment(self.makeSym("x"), self.makeSym("y"),\
            self.makeSym("xd"),self.makeSym("yd"),self.makeSym("th"),\
            self.makeSym("thd"), self.objId, self.m, self.I, self.r,\
            self.getLength(), self.fixed)
        return node, [(node.x, node.xd), (node.y, node.yd), (node.th, node.thd)]
    @staticmethod
    def maybeValidRatio(num):
        if num >= 0.0 and num <= 1.0:
            return num
        else:
            raise AttributeError("%f out of bounds, should be between 0 and 1"\
                % num)

Drawable.register(Point)
Drawable.register(Segment)

# Testing
#surface = pg.display.set_mode((640, 480))
#surface.fill(whiteColor)
#point = Point(surface, 100, 100, 2.4, True, 10)
#segment = Segment(surface, 100, 100, 200, 200, 3.2, 0.75, 5.2, True)
#segment.setRatioDistanceToCentroid(1.5)
#collection = [point, segment]
#translation = [obj.translate() for obj in collection]
#print translation[0].__dict__
#print translation[1].__dict__
#point.draw()
#while True:
#    pg.display.update()
