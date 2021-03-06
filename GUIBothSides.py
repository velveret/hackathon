import pygame
import wx
import os
import Buttons
from math import ceil, pi, sin, cos, sqrt, atan2
from Drawable import Point, Segment

#Buttons
""" 
(IDs)
1  ==> Cartesian
2  ==> Polar
3  ==> Snap To Grid
4  ==> Snap To Point
5  ==> Run
6  ==> Pause
7  ==> Restart
8  ==> Point
9  ==> Segment
10 ==> Undo

(List)
0  ==> Cartesian
1  ==> Polar
2  ==> Snap To Grid
3  ==> Snap To Point
4  ==> Restart
5  ==> Run
6  ==> Pause
7  ==> Point
8  ==> Segment
9  ==> Undo
"""

class GraphicsScreen(pygame.Surface):
    def __init__(self, size, buttons):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.buttons = buttons
        
        self.pointAdding = False
        
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
                        
        self.buttons[0].setState(self.cartesian)
        self.buttons[1].setState(self.polar)
        self.buttons[2].setState(self.snapGrid)
        self.buttons[3].setState(self.snapPoint)
        
        self.allGeometry = []
        
    def buttonPressed(self, buttonID):
        if buttonID == 1: #Cartesian
            self.cartesian = True
            self.polar = False
            self.buttons[0].setState(True)
            self.buttons[1].setState(False)
            
        elif buttonID == 2: #Polar
            self.cartesian = False
            self.polar = True
            self.buttons[0].setState(False)
            self.buttons[1].setState(True)
            
        elif buttonID == 3: #Snap To Grid
            self.snapGrid = not self.snapGrid
            self.buttons[2].setState(self.snapGrid)
            
        elif buttonID == 4: #Snap To Point
            self.snapPoint = not self.snapPoint
            self.buttons[3].setState(self.snapPoint)
            
            
        if buttonID == 8: #Point Adding
            if self.pointAdding:
                self.pointAdding = False
            else:
                self.pointAdding = True
                self.segmentAdding = False
                self.buttons[8].setState(False)
            self.buttons[7].setState(self.pointAdding)
            
        elif buttonID == 9: #Segment Adding
            if self.segmentAdding:
                self.segmentAdding = False
            else:
                self.segmentAdding = True
                self.pointAdding = False
                self.buttons[7].setState(False)
            self.buttons[8].setState(self.segmentAdding)
            
        elif buttonID == 10: #Undo
            if len(self.allGeometry) > 0:
                self.allGeometry.pop()    
            self.buttons[9].setState(True)
            
    def snap(self, x, y):
        if self.snapGrid:        
            if self.cartesian:
                x = int(round(float(x)/self.cartesianSpacing)*self.cartesianSpacing)
                y = int(round(float(y)/self.cartesianSpacing)*self.cartesianSpacing)
            elif self.polar:
                r = self.dist((x,y), self.polarOrigin)
                theta = atan2(y-self.polarOrigin[1], x-self.polarOrigin[0])
                r = int(round(float(r)/self.polarRSpacing)*self.polarRSpacing)
                theta = round(theta/self.polarThetaSpacing)*self.polarThetaSpacing
                x = int(r*cos(theta)) + self.polarOrigin[0]
                y = int(r*sin(theta)) + self.polarOrigin[1]
        
        return x, y
        
    def addPoint(self, x, y):
        newPoint = Point(self, x, y)
        self.allGeometry.append(newPoint)
        
    def startSegment(self, x, y):
        self.currentSegment = Segment(self, x, y, x, y)
        self.segmentAddingStage = 1
        self.allGeometry.append(self.currentSegment)
    
    def updateSegment(self, x, y):
        self.currentSegment.setX1(x)
        self.currentSegment.setY1(y)
        
    def finishSegment(self, x, y):
        self.currentSegment.setX1(x)
        self.currentSegment.setY1(y)
        self.segmentAddingStage = 0
        del(self.currentSegment)
            
    def mousePressed(self, mx, my):
        if self.pointAdding:
            mx, my = self.snap(mx, my)
            self.addPoint(mx,my)
        elif self.segmentAdding:
            mx, my = self.snap(mx, my)
            self.startSegment(mx, my)
            
    def mouseReleased(self, mx, my):
        if self.segmentAdding and self.segmentAddingStage == 1:
            mx, my = self.snap(mx, my)
            self.finishSegment(mx, my)

    def mouseMoved(self, mx, my):
        if self.segmentAdding and self.segmentAddingStage == 1:
            mx, my = self.snap(mx, my)
            self.updateSegment(mx, my)            
    
    def doStuff(self):
        pass
    
    def updateSize(self, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        
    def dist(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        return sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def draw(self):
        
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
                
        for drawable in self.allGeometry:
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
        
        self.buttons = []
        
        self.cartesianGridButton = Buttons.CartesianGridButton()
        self.buttons.append(self.cartesianGridButton)
        
        self.polarGridButton = Buttons.PolarGridButton()
        self.buttons.append(self.polarGridButton)
        
        self.snapToGridButton = Buttons.SnapToGridButton()
        self.buttons.append(self.snapToGridButton)
        
        self.snapToPointButton = Buttons.SnapToPointButton()
        self.buttons.append(self.snapToPointButton)
        
        self.restartButton = Buttons.RestartButton()
        self.buttons.append(self.restartButton)
        
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        
        self.pauseButton = Buttons.PauseButton()
        self.buttons.append(self.pauseButton)
                
        self.pointButton = Buttons.PointButton()
        self.buttons.append(self.pointButton)
        
        self.segmentButton = Buttons.SegmentButton()
        self.buttons.append(self.segmentButton)
        
        self.undoButton = Buttons.UndoButton()
        self.buttons.append(self.undoButton)
        
        self.pinButton = Buttons.PinButton()
        self.buttons.append(self.pinButton)
        
        self.deleteButton = Buttons.DeleteButton()
        self.buttons.append(self.deleteButton)
        
        numButtons = len(self.buttons)
                
        self.buttonsOnLeft = int(ceil(numButtons/2.0))
        
        self.buttonSize = (self.size[1]-20) / self.buttonsOnLeft
        
        self.buttonSize -= self.buttonSpacing        
        
        self.graphics = GraphicsScreen((self.size[0] - 2*int(self.buttonSize*1.2), self.size[1]), self.buttons)
        
        self.setSizes()
        
    def setSizes(self):
        self.leftPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.leftPanelPos = (0,0)
        
        self.rightPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.rightPanelPos = (self.size[0]-self.rightPanel.get_size()[0],0)
        
        self.graphicsPos =  (self.leftPanel.get_size()[0],0)
        self.graphicsSize = (self.size[0] - 2*int(self.buttonSize*1.2), self.size[1])
        self.graphics.updateSize(self.graphicsSize)
        
        cur = 0
        for i in range(self.buttonsOnLeft):
            self.buttons[i].setPos(self.leftPanel, self.leftPanelPos[0], self.leftPanelPos[1], 0, cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
        
        cur = 0
        for i in range(self.buttonsOnLeft, len(self.buttons)):
            self.buttons[i].setPos(self.rightPanel, self.rightPanelPos[0], self.rightPanelPos[1], int(self.buttonSize*0.2), cur, self.buttonSize, self.buttonSize)
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
            for button in self.buttons:
                buttonID = button.testButton(mx, my)
                if buttonID != 0:
                    self.graphics.buttonPressed(buttonID)
        
    def onMouseReleased(self):
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
        self.graphics.fill((0,255,0))
        self.graphics.draw()
        
        self.leftPanel.fill((200,200,200))
        self.rightPanel.fill((200,200,200))
        
                
        for button in self.buttons:
            button.draw()    
        
        self.screen.blit(self.leftPanel, (0,0))
        self.screen.blit(self.rightPanel, self.rightPanelPos)
        self.screen.blit(self.graphics, self.graphicsPos)

        pygame.display.update()

    def onPaint(self, event):
        self.Redraw()
 
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

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        filemenu.AppendSeparator()
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



