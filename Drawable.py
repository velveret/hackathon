# -*- coding: utf-8 -*-
from abc import abstractmethod
from abc import ABCMeta
import pygame as pg
import numpy as np
from math import atan2,sin,cos

pg.init()
blackColor = pg.Color(0, 0, 0)
blueColor = pg.Color(0, 0, 255)
whiteColor = pg.Color(255, 255, 255)

class Drawable(object):
    __metaclass__ = ABCMeta
    x = 0.0
    y = 0.0
    def __init__(self, newX, newY):
        self.x = newX
        self.y = newY
    @abstractmethod
    def draw(self, surface):
        pass
    def setX(self, newX):
        self.x = newX
    def setY(self, newY):
        self.y = newY

class Point(Drawable):
    r = 0.0
    def __init__(self, newX, newY, newR):
        super(Point, self).__init__(newX, newY)
        self.r = newR
    def draw(self, surface):
        pg.draw.circle(surface, blackColor, (self.x, self.y), self.r)
    def setR(self, newR):
        self.r = newR

class Segment(Drawable):
    x1 = 0.0
    y1 = 0.0
    def __init__(self, x0, y0, newX1, newY1):
        super(Segment, self).__init__(x0, y0)
        self.x0 = x0
        self.y0 = y0
        self.x1 = newX1
        self.y1 = newY1
    def draw(self, surface):
        pg.draw.line(surface, blueColor, (self.x0, self.y0), (self.x1, self.y1))
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
    def rotate(self, theta, switch=False):
        if switch:
            newX = self.x0 - self.x1
            newY = self.y0 - self.y1  
            newX, newY = newX * cos(theta) - newY * sin(theta) + self.x1, newX * sin(theta) + newY * cos(theta) + self.y1
            self.setX0(newX)
            self.setY0(newY)
        else:
            newX = self.x1 - self.x0
            newY = self.y1 - self.y0  
            newX, newY = newX * cos(theta) - newY * sin(theta) + self.x0, newX * sin(theta) + newY * cos(theta) + self.y0
            self.setX1(newX)
            self.setY1(newY)

Drawable.register(Point)
Drawable.register(Segment)
    