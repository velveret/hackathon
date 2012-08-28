import pygame
import wx
import os
import Buttons
from math import pi, sin, cos, sqrt, atan2
from Drawable import Point, Segment, StaticDrawing
from driver_01 import Driver
from copy import copy
from AnimationPositionFinder import AnimationPositions


class DisplayLagrangeWindow(wx.Frame):
    def __init__(self, parent, title, lagrange):
        wx.Frame.__init__(self, parent, title=title, size=(500,500))
        self.control = wx.TextCtrl(self, style=wx.TE_READONLY+wx.TE_MULTILINE)
        for part in lagrange:
            self.control.AppendText(str(part)+" = 0\n\n")
        self.Show(True)

class GraphicsScreen(pygame.Surface):
    def __init__(self, size, buttons):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.buttons = buttons
        
        self.pointAdding = False
        self.pinAdding = False
        
        self.segmentAdding = False
        self.segmentAddingStage = 0
        
        self.snapGrid = True
        
        self.snapPoint = True
        
        self.cartesian = True
        self.cartesianOrigin = (self.size[0]/2,self.size[1]/2)
        self.cartesianSpacing = 20
        
        self.polar = False
        self.polarOrigin = (self.size[0]/2,self.size[1]/2)
        self.polarRSpacing = 20
        self.polarThetaSpacing = pi/12
                        
        self.buttons["cartesianGrid"].setState(self.cartesian)
        self.buttons["polarGrid"].setState(self.polar)
        self.buttons["snapToGrid"].setState(self.snapGrid)
        self.buttons["snapToPoint"].setState(self.snapPoint)
        
        self.origin = self.polarOrigin
        
        self.allGeometry = []
        self.prevGeometry = []
        self.runningGeometry = []
        
        self.runningSimulation = False
        self.simulationPaused = False
        
        
    def runSimulationStart(self):
        self.runningGeometry = []
        for drawable in self.allGeometry:
            self.runningGeometry.append(copy(drawable))
        self.anim = AnimationPositions()
        self.runningSimulation = True
        
        self.geom = self.anim.dfs(self.diagram, self.anim.find_head(self.diagram), self.traj, self.varList, self.runningGeometry, self.origin)

#        for geom in anim.dfs(self.diagram, anim.find_head(self.diagram), self.traj, self.varList, self.runningGeometry, self.origin):
#            print geom
#            for node in geom:
#                print node.__dict__
#            self.draw(geom)

    def simulationFrame(self):
        if not self.simulationPaused:
            try:
                self.runningGeometry = self.geom.next()
            except:
                self.buttons["run"].setState(False)
                self.runningSimulation = False
                return
#        print self.runningGeometry
#        for node in self.runningGeometry:
#            print node.__dict__
#        self.draw(geom)            
    
    def buttonPressed(self, buttonID):
        if buttonID == "cartesianGrid":
            self.cartesian = True
            self.polar = False
            self.buttons["cartesianGrid"].setState(True)
            self.buttons["polarGrid"].setState(False)
            
        elif buttonID == "polarGrid":
            self.cartesian = False
            self.polar = True
            self.buttons["cartesianGrid"].setState(False)
            self.buttons["polarGrid"].setState(True)
            
        elif buttonID == "snapToGrid":
            self.snapGrid = not self.snapGrid
            self.buttons["snapToGrid"].setState(self.snapGrid)
            
        elif buttonID == "snapToPoint":
            self.snapPoint = not self.snapPoint
            self.buttons["snapToPoint"].setState(self.snapPoint)
            
            
        elif buttonID == "point":
            if self.pointAdding:
                self.pointAdding = False
            else:
                self.pointAdding = True
                self.pinAdding = False
                self.segmentAdding = False
                self.buttons["pin"].setState(False)
                self.buttons["segment"].setState(False)
            self.buttons["point"].setState(self.pointAdding)
            
        elif buttonID == "pin":
            if self.pinAdding:
                self.pinAdding = False
            else:
                self.pinAdding = True
                self.segmentAdding = False
                self.pointAdding = False
                self.buttons["point"].setState(False)
                self.buttons["segment"].setState(False)
            self.buttons["pin"].setState(self.pinAdding)
            
        elif buttonID == "segment":
            if self.segmentAdding:
                self.segmentAdding = False
            else:
                self.segmentAdding = True
                self.pointAdding = False
                self.pinAdding = False
                self.buttons["point"].setState(False)
                self.buttons["pin"].setState(False)
            self.buttons["segment"].setState(self.segmentAdding)
            
        elif buttonID == "undo":
            if len(self.allGeometry) > 0:
                self.allGeometry.pop()
            elif len(self.prevGeometry) > 0:
                for geom in self.prevGeometry:
                    self.allGeometry.append(geom)
                self.prevGeometry = []
            self.buttons["undo"].setState(True)
            
        elif buttonID == "delete":
            if len(self.allGeometry) > 0:
                for geom in self.allGeometry:
                    self.prevGeometry.append(geom)
                self.allGeometry = []
            self.buttons["delete"].setState(True)
            
        elif buttonID == "run":
            if not self.runningSimulation:
                if len(self.allGeometry) > 0:
                    self.diagram, self.varList, self.angleDict = StaticDrawing.makeDiagram(self.allGeometry, self.origin)
                    self.traj, tempLag = Driver.drive(self.diagram, self.varList, self.angleDict)
                    frame = DisplayLagrangeWindow(None, "Euler-Lagrange Equations", tempLag)
#                    app.MainLoop()
                    self.runSimulationStart()
                self.buttons["run"].setState(True)
            else:
                if self.simulationPaused:
                    self.simulationPaused = False
                    self.buttons["pause"].setState(False)
            
        elif buttonID == "pause":
            if self.runningSimulation:
                self.simulationPaused = not self.simulationPaused
            self.buttons["pause"].setState(self.simulationPaused)
            
        elif buttonID == "restart":
            if self.runningSimulation:
                self.runningSimulation = False
                self.buttons["run"].setState(False)
                self.buttons["pause"].setState(False)
            
    def snap(self, x, y, objToSnapTo):
        snapped = False
        if self.snapPoint:
            for geom in self.allGeometry:
                if isinstance(geom, objToSnapTo):
                    if objToSnapTo == Segment:
                        if self.dist((x,y), (geom.x0, geom.y0)) < 50 and self.dist((x,y), (geom.x1, geom.y1)) < 50:
                            if self.dist((x,y), (geom.x0, geom.y0)) < self.dist((x,y), (geom.x1, geom.y1)):
                                x,y = geom.x0, geom.y0
                            else:
                                x,y = geom.x1, geom.y1
                            snapped = True
                        elif self.dist((x,y), (geom.x0, geom.y0)) < 50:
                            x,y = geom.x0, geom.y0
                            snapped = True
                        elif self.dist((x,y), (geom.x1, geom.y1)) < 50:
                            x,y = geom.x1, geom.y1
                            snapped = True
                    else:
                        if self.dist((x,y), (geom.x, geom.y)) < 50:
                            x, y = geom.x, geom.y
                            snapped = True
                                
        if self.snapGrid and not snapped:        
            if self.cartesian:
                x -= self.cartesianOrigin[0]
                y -= self.cartesianOrigin[1]
                x = int(round(float(x)/self.cartesianSpacing)*self.cartesianSpacing)
                y = int(round(float(y)/self.cartesianSpacing)*self.cartesianSpacing)
                x += self.cartesianOrigin[0]
                y += self.cartesianOrigin[1]
            elif self.polar:
                r = self.dist((x,y), self.polarOrigin)
                theta = atan2(y-self.polarOrigin[1], x-self.polarOrigin[0])
                r = int(round(float(r)/self.polarRSpacing)*self.polarRSpacing)
                theta = round(theta/self.polarThetaSpacing)*self.polarThetaSpacing
                x = int(r*cos(theta)) + self.polarOrigin[0]
                y = int(r*sin(theta)) + self.polarOrigin[1]
        
        return x, y
        
    def addPoint(self, x, y):
        x, y = self.snap(x, y, Segment)
        newPoint = Point(self, x, y)
        self.allGeometry.append(newPoint)
        
    def addPin(self, x, y):
        x, y = self.snap(x, y, Segment)
        newPoint = Point(self, x, y, isFixed=True)
        self.allGeometry.append(newPoint)
        
    def startSegment(self, x, y):
        x, y = self.snap(x, y, Point)
        self.currentSegment = Segment(self, x, y, x, y)
        self.segmentAddingStage = 1
        self.allGeometry.append(self.currentSegment)
    
    def updateSegment(self, x, y):
        x, y = self.snap(x, y, Point)
        self.currentSegment.setX1(x)
        self.currentSegment.setY1(y)
        
    def finishSegment(self, x, y):
        x, y = self.snap(x, y, Point)
        self.currentSegment.setX1(x)
        self.currentSegment.setY1(y)
        self.segmentAddingStage = 0
        del(self.currentSegment)
            
    def mousePressed(self, mx, my):
        if self.pointAdding:
            self.addPoint(mx,my)
        elif self.pinAdding:
            self.addPin(mx,my)
        elif self.segmentAdding:
            self.startSegment(mx, my)
            
    def mouseReleased(self, mx, my):
        if self.segmentAdding and self.segmentAddingStage == 1:
            self.finishSegment(mx, my)

    def mouseMoved(self, mx, my):
        if self.segmentAdding and self.segmentAddingStage == 1:
            self.updateSegment(mx, my)            
    
    def updateSize(self, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        
    def dist(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        return sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def draw(self, geom=None):
        
        if self.runningSimulation:
            self.simulationFrame()
        
        if self.cartesian:
            pygame.draw.line(self, (0,0,0), (self.cartesianOrigin[0], -10000), (self.cartesianOrigin[0], 10000), 3)
            pygame.draw.line(self, (0,0,0), (-10000, self.cartesianOrigin[1]), (10000, self.cartesianOrigin[1]), 3)
            
            cur = self.cartesianOrigin[0] + self.cartesianSpacing
            while cur < self.size[0]:
                pygame.draw.line(self, (0,0,0), (cur, -10000), (cur, 10000), 1)
                cur += self.cartesianSpacing
                
            cur = self.cartesianOrigin[0] - self.cartesianSpacing
            while cur > 0:
                pygame.draw.line(self, (0,0,0), (cur, -10000), (cur, 10000), 1)
                cur -= self.cartesianSpacing
                
            cur = self.cartesianOrigin[1] + self.cartesianSpacing
            while cur < self.size[1]:
                pygame.draw.line(self, (0,0,0), (-10000, cur), (10000, cur), 1)
                cur += self.cartesianSpacing
                
            cur = self.cartesianOrigin[1] - self.cartesianSpacing
            while cur > 0:
                pygame.draw.line(self, (0,0,0), (-10000, cur), (10000, cur), 1)
                cur -= self.cartesianSpacing
            
        elif self.polar:
#            pygame.draw.line(self, (0,0,0), (self.polarOrigin[0], -10000), (self.polarOrigin[0], 10000), 3)
#            pygame.draw.line(self, (0,0,0), (-10000, self.polarOrigin[1]), (10000, self.polarOrigin[1]), 3)
            
            for i in range(12):
                angle = pi*i/12.0
                x1 = cos(angle)*-10000 + self.polarOrigin[0]
                y1 = sin(angle)*-10000 + self.polarOrigin[1]
                
                x2 = cos(angle)*10000 + self.polarOrigin[0]
                y2 = sin(angle)*10000 + self.polarOrigin[1]
                
                if i==0 or i==6:
                    pygame.draw.line(self, (0,0,0), (x1, y1), (x2, y2), 3)
                else:
                    pygame.draw.line(self, (0,0,0), (x1, y1), (x2, y2), 1)
            
            dist1 = self.dist(self.polarOrigin, (0,0))
            dist2 = self.dist(self.polarOrigin, (self.size[0], 0))
            dist3 = self.dist(self.polarOrigin, (0, self.size[1]))
            dist4 = self.dist(self.polarOrigin, (self.size[0], self.size[1]))
            
            dist = max([dist1, dist2, dist3, dist4])            
            
            cur = self.polarRSpacing
            while cur <= dist:
                pygame.draw.circle(self, (0,0,0), self.polarOrigin, cur, 1)
                cur += self.polarRSpacing
                
        segments = []
        points = []
        if not self.runningSimulation:
            for drawable in self.allGeometry:
                if isinstance(drawable, Segment):
                    segments.append(drawable)
                else:
                    points.append(drawable)
            
            for drawable in segments:
                drawable.draw()
                
            for drawable in points:
                drawable.draw()
        else:
#            print "drawing new geom"
            for drawable in self.runningGeometry:
                drawable.draw()
    
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        os.environ['SDL_WINDOWID'] = str(self.hwnd)
       
        self.mouseDown = False       
       
        pygame.display.init()
        pygame.display.set_icon(pygame.image.load('images/icon.png'))
        self.screen = pygame.display.set_mode()
        self.size = self.GetSizeTuple()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)
        
        self.buttonSpacing = 10
        
        self.buttons = {}
        
        self.cartesianGridButton = Buttons.CartesianGridButton()
        self.buttons["cartesianGrid"] = self.cartesianGridButton
#        self.buttons.append(self.cartesianGridButton)
        
        self.polarGridButton = Buttons.PolarGridButton()
        self.buttons["polarGrid"] = self.polarGridButton
#        self.buttons.append(self.polarGridButton)
        
        self.snapToGridButton = Buttons.SnapToGridButton()
        self.buttons["snapToGrid"] = self.snapToGridButton
#        self.buttons.append(self.snapToGridButton)
        
        self.snapToPointButton = Buttons.SnapToPointButton()
        self.buttons["snapToPoint"] = self.snapToPointButton
#        self.buttons.append(self.snapToPointButton)
        
        self.restartButton = Buttons.RestartButton()
        self.buttons["restart"] = self.restartButton
#        self.buttons.append(self.restartButton)
        
        self.runButton = Buttons.RunButton()
        self.buttons["run"] = self.runButton
#        self.buttons.append(self.runButton)
        
        self.pauseButton = Buttons.PauseButton()
        self.buttons["pause"] = self.pauseButton
#        self.buttons.append(self.pauseButton)
                
        self.pointButton = Buttons.PointButton()
        self.buttons["point"] = self.pointButton
#        self.buttons.append(self.pointButton)
        
        self.segmentButton = Buttons.SegmentButton()
        self.buttons["segment"] = self.segmentButton
#        self.buttons.append(self.segmentButton)
        
        self.undoButton = Buttons.UndoButton()
        self.buttons["undo"] = self.undoButton
#        self.buttons.append(self.undoButton)
        
        self.pinButton = Buttons.PinButton()
        self.buttons["pin"] = self.pinButton
#        self.buttons.append(self.pinButton)
        
        self.deleteButton = Buttons.DeleteButton()
        self.buttons["delete"] = self.deleteButton
#        self.buttons.append(self.deleteButton)

        self.leftButtons = ["cartesianGrid", "snapToGrid", "segment", "pin", "pause", "undo"]
        self.rightButtons = ["polarGrid", "snapToPoint", "point", "run", "restart", "delete"]
                                
        self.buttonSize = (self.size[1]-20) / max(len(self.leftButtons), len(self.rightButtons))
        
        self.buttonSize -= self.buttonSpacing        
        
        self.graphics = GraphicsScreen((self.size[0] - 2*int(self.buttonSize*1.2), self.size[1]), self.buttons)
        
        self.setSizes()
        
    def setSizes(self):
        self.leftPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.leftPanelPos = (0,0)
        
        self.rightPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.rightPanelPos = (int(self.buttonSize*1.2),0)
        
        self.graphicsPos =  (self.leftPanel.get_size()[0] + self.rightPanel.get_size()[0],0)
        self.graphicsSize = (self.size[0] - 2*int(self.buttonSize*1.2), self.size[1])
        self.graphics.updateSize(self.graphicsSize)
        
        cur = 0
        for key in self.leftButtons:
            self.buttons[key].setPos(self.leftPanel, self.leftPanelPos[0], self.leftPanelPos[1], 0, cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
        
        cur = 0
        for key in self.rightButtons:
            self.buttons[key].setPos(self.rightPanel, self.rightPanelPos[0], self.rightPanelPos[1], 0, cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
 
    def update(self, event):
        self.onMouseMoved()
        
        if pygame.mouse.get_pressed()[0]:
            if not self.mouseDown:
                self.mouseDown = True
                self.onMousePressed()
        else:
            if self.mouseDown:
                self.mouseDown = False
                self.onMouseReleased()
        
        self.redraw()
        
    def onMousePressed(self):
        (mx, my) = pygame.mouse.get_pos()
        
        if (mx >= self.graphicsPos[0] and mx <= self.graphicsPos[0]+self.graphicsSize[0]) and (my >= self.graphicsPos[1] and my <= self.graphicsPos[1]+self.graphicsSize[1]):
            self.graphics.mousePressed(mx-self.graphicsPos[0], my-self.graphicsPos[1])
        else:
            for buttonKey in self.buttons.keys():
                buttonID = self.buttons[buttonKey].testButton(mx, my)
                if buttonID != 0:
                    self.graphics.buttonPressed(buttonID)
        
    def onMouseReleased(self):
        self.buttons["undo"].setState(False)
        self.buttons["delete"].setState(False)
#        self.buttons["run"].setState(False)
#        self.buttons["pause"].setState(False)
        self.buttons["restart"].setState(False)
        
        
        (mx, my) = pygame.mouse.get_pos()
        
        if (mx >= self.graphicsPos[0] and mx <= self.graphicsPos[0]+self.graphicsSize[0]) and (my >= self.graphicsPos[1] and my <= self.graphicsPos[1]+self.graphicsSize[1]):
            self.graphics.mouseReleased(mx-self.graphicsPos[0], my-self.graphicsPos[1])
        
    def onMouseMoved(self):
        (mx, my) = pygame.mouse.get_pos()
        
        if (mx >= self.graphicsPos[0] and mx <= self.graphicsPos[0]+self.graphicsSize[0]) and (my >= self.graphicsPos[1] and my <= self.graphicsPos[1]+self.graphicsSize[1]):
            self.graphics.mouseMoved(mx-self.graphicsPos[0], my-self.graphicsPos[1])

    def redraw(self):
        self.screen.fill((255, 255, 255))
        
#        self.graphics.fill((255,255,255))
        self.graphics.fill((220,220,220))
        self.graphics.draw()
        
        self.leftPanel.fill((100,100,100))
        self.rightPanel.fill((100,100,100))
        
                
        for buttonKey in self.buttons.keys():
            self.buttons[buttonKey].draw()    
        
        self.screen.blit(self.leftPanel, (0,0))
        self.screen.blit(self.rightPanel, self.rightPanelPos)
        self.screen.blit(self.graphics, self.graphicsPos)

        pygame.display.update()

    def onPaint(self, event):
        self.redraw()
 
    def onSize(self, event):
        self.size = self.GetSizeTuple()
        
#        Failed attemps to make it not break when it gets to small
#        if self.size[0] < 500 or self.size[1] < 300:
#            print "fixing"
#            self.SetDimensions(-1, -1, self.sizePrev[0], self.sizePrev[1])
#        else:
#            self.sizePrev = self.size
#            
#        print self.sizePrev
        
        
        self.setSizes()
 
    def kill(self, event):
        self.Unbind(event=wx.EVT_PAINT, handler=self.onPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.update, source=self.timer)

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        screenGeom = wx.Display(0).GetGeometry()
        screenSize = [screenGeom[2]-screenGeom[0], screenGeom[3]-screenGeom[1]]
        wx.Frame.__init__(self, parent, title=title, size=(screenSize[0]-100,screenSize[1]-100), pos=(50,25))
        self.CreateStatusBar()
        
        self.display = PygameDisplay(self, -1)

        filemenu= wx.Menu()

#        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
#        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
#        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)
        self.Show(True)
        
    def onAbout(self, event):
        print "OUTPUTS"
        
    def onExit(self, event):
#        sys.exit()
        self.display.kill(event)
        pygame.quit()
        self.Destroy()
    

if __name__ == "__main__":
    app = wx.App(0)
    
    frame = MainWindow(None, "PhySim")
    frame.Show(True)
    app.MainLoop()



