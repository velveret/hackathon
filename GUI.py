import pygame
import wx
import os
import Buttons
from math import ceil

class GraphicsScreen(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
    
    def doStuff(self):
        pass
    
    def updateSize(self):
        self.size = 0
    
    def draw(self):
        
        for i in range(50):
            pygame.draw.line(self, (0,0,0), (0, i*10), (100, i*10), 1)
            
    
    
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
        
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        self.runButton = Buttons.RunButton()
        self.buttons.append(self.runButton)
        
        self.setSizes()
        
        self.mouseDown = False
        
        self.graphics = GraphicsScreen((self.size[0] - 2*int(self.buttonSize*1.2), self.size[1]))
        
    def onMouse(self, event):
        print "MOUSE SHIT"
        
    def setSizes(self):
        numButtons = len(self.buttons)
                
        buttonsOnLeft = int(ceil(numButtons/2.0))
        
        self.buttonSize = (self.size[1]-20) / buttonsOnLeft
        
        self.buttonSize -= self.buttonSpacing
        
#        print "Size =", self.buttonSize
                
        self.leftPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.leftPanelPos = (0,0)
        
        self.rightPanel = pygame.Surface((int(self.buttonSize*1.2), self.size[1]))
        self.rightPanelPos = (self.size[0]-self.rightPanel.get_size()[0],0)
        
        self.graphicsPos =  (self.leftPanel.get_size()[0],0)
        
        cur = 0
        for i in range(buttonsOnLeft):
            self.buttons[i].setPos(self.leftPanel, self.leftPanelPos[0], self.leftPanelPos[1], 0, cur, self.buttonSize, self.buttonSize)
            cur += self.buttonSize + self.buttonSpacing
#            print "added on left", cur
        
        cur = 0
        for i in range(buttonsOnLeft, len(self.buttons)):
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
        print "Testing"
        (mx, my) = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.testButton(mx, my):
                print "Got one"
        
    def onMouseReleased(self):
        pass
 
    def redraw(self):
        self.screen.fill((255, 255, 255))
        
        self.graphics.fill((255,255,255))
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



