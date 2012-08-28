import pygame

class Button:
    def __init__(self):
        self.backColor = (255,0,0)
        
    def setPos(self, parentSurface, panelx, panely, x, y, w, h):
        ratio = 0.9
        self.parentSurface = parentSurface
        self.backx = x
        self.backy = y
        self.iconx = x + w*((1-ratio)/2.0)
        self.icony = y + h*((1-ratio)/2.0)
        self.w = w
        self.h = h
#        print "Added at", x, y
        self.icon = pygame.transform.smoothscale(self.icon, (int(w*ratio), int(h*ratio)))
        self.back = pygame.Surface((w,h))
        self.back.fill(self.backColor)
        self.actualx = panelx + x
        self.actualy = panely + y
    
    def draw(self):
        self.back.fill(self.backColor)
        self.parentSurface.blit(self.back, (self.backx, self.backy))
        self.parentSurface.blit(self.icon, (self.iconx, self.icony))
        
    def testButton(self, mx, my):
        xmin = self.actualx
        xmax = xmin + self.w
        ymin = self.actualy
        ymax = ymin + self.h
        if (mx >= xmin and mx <= xmax) and (my >= ymin and my <= ymax):
            return self.ID
        else:
            return 0
            
    def setState(self, active):
        if active:
            self.active = True
            self.backColor = (0,0,255)
        else:
            self.active = False
            self.backColor = (255,0,0)

class CartesianGridButton(Button):
    def __init__(self):
        self.active = True
        self.icon = pygame.image.load('images/gridIcon.png').convert()
        self.ID = 1
        Button.__init__(self)
        
class PolarGridButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/polarIcon.png').convert()
        self.ID = 2
        Button.__init__(self)
        
class SnapToGridButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/snapIcon.png').convert()
        self.ID = 3
        Button.__init__(self)
        
class SnapToPointButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/snapPointIcon.png').convert()
        self.ID = 4
        Button.__init__(self)
        
class RunButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/runIcon.png').convert()
        self.ID = 5
        Button.__init__(self)
        
class PauseButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/pauseIcon.png').convert()
        self.ID = 6
        Button.__init__(self)
        
class RestartButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/restartIcon.png').convert()
        self.ID = 7
        Button.__init__(self)
        
class PointButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/pointIcon.png').convert()
        self.ID = 8
        Button.__init__(self)
        
class SegmentButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/segmentIcon.png').convert()
        self.ID = 9
        Button.__init__(self)
        
class UndoButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/undoIcon.png').convert()
        self.ID = 10
        Button.__init__(self)

class PinButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/pinIcon.png').convert()
        self.ID = 11
        Button.__init__(self)
        
class DeleteButton(Button):
    def __init__(self):
        self.active = False
        self.icon = pygame.image.load('images/deleteIcon.png').convert()
        self.ID = 12
        Button.__init__(self)