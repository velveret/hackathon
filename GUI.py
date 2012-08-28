import pygame
import wx
import os
import Buttons
from math import ceil, pi, sin, cos, sqrt

class GraphicsScreen(pygame.Surface):
    def __init__(self, size, buttons):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.buttons = buttons
        
        self.snap = True
        
        self.cartesian = True
        self.cartesianOrigin = (100,100)
        
        self.polar = False
        self.polarOrigin = (300,300)
        
    def buttonPressed(self, buttonID):
        if buttonID == 1:
            self.cartesian = True
            self.polar = False
            self.buttons[0].setState(True)
            self.buttons[1].setState(False)
            
        elif buttonID == 2:
            self.cartesian = False
            self.polar = True
            self.buttons[0].setState(False)
            self.buttons[1].setState(True)
    
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
            
            cur = self.cartesianOrigin[0]
            while cur < self.size[0]:
                pygame.draw.line(self, (0,0,0), (cur, -10000), (cur, 10000), 1)
                cur += 20
                
            cur = self.cartesianOrigin[0]
            while cur > 0:
                pygame.draw.line(self, (0,0,0), (cur, -10000), (cur, 10000), 1)
                cur -= 20
                
            cur = self.cartesianOrigin[1]
            while cur < self.size[1]:
                pygame.draw.line(self, (0,0,0), (-10000, cur), (10000, cur), 1)
                cur += 20
                
            cur = self.cartesianOrigin[1]
            while cur > 0:
                pygame.draw.line(self, (0,0,0), (-10000, cur), (10000, cur), 1)
                cur -= 20
            
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
            
            cur = 20
            while cur <= dist:
                pygame.draw.circle(self, (0,0,0), self.polarOrigin, cur, 1)
                cur += 20
            
            
#            for i in range(50):
#                pygame.draw.line(self, (0,0,0), (0, i*10), (100, i*10), 1)
            
    
    
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        os.environ['SDL_WINDOWID'] = str(self.hwnd)
       
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
        
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        
        self.pauseButton = Buttons.PauseButton()
        self.buttons.append(self.pauseButton)
        
        self.restartButton = Buttons.RestartButton()
        self.buttons.append(self.restartButton)
        
        self.pointButton = Buttons.PointButton()
        self.buttons.append(self.pointButton)
        
        self.segmentButton = Buttons.SegmentButton()
        self.buttons.append(self.segmentButton)
        
        self.undoButton = Buttons.UndoButton()
        self.buttons.append(self.undoButton)
        
        numButtons = len(self.buttons)
                
        self.buttonsOnLeft = int(ceil(numButtons/2.0))
        
        self.buttonSize = (self.size[1]-20) / self.buttonsOnLeft
        
        self.buttonSize -= self.buttonSpacing        
        
        self.graphics = GraphicsScreen((self.size[0] - 2*int(self.buttonSize*1.2), self.size[1]), self.buttons)
        
        self.setSizes()
        
        self.mouseDown = False
        
        
    def onMouse(self, event):
        print "MOUSE SHIT"
        
    def setSizes(self):

        
#        print "Size =", self.buttonSize
                
        self.leftPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.leftPanelPos = (0,0)
        
        self.rightPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.rightPanelPos = (self.size[0]-self.rightPanel.get_size()[0],0)
        
        self.graphicsPos =  (self.leftPanel.get_size()[0],0)
        self.graphics.updateSize((self.size[0] - 2*int(self.buttonSize*1.2), self.size[1]))
        
        cur = 0
        for i in range(self.buttonsOnLeft):
            self.buttons[i].setPos(self.leftPanel, self.leftPanelPos[0], self.leftPanelPos[1], 0, cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
#            print "added on left", cur
        
        cur = 0
        for i in range(self.buttonsOnLeft, len(self.buttons)):
            self.buttons[i].setPos(self.rightPanel, self.rightPanelPos[0], self.rightPanelPos[1], int(self.buttonSize*0.2), cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
#            print "added on right", cur
 
    def update(self, event):
#        self.graphics.update()

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
        for button in self.buttons:
            buttonID = button.testButton(mx, my)
            if buttonID != 0:
                self.graphics.buttonPressed(buttonID)
        
    def onMouseReleased(self):
        pass
 
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



