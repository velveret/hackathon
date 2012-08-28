import pygame

class Button:
#    def __init__(self, ):
        
    def setPos(self, parentSurface, panelx, panely, x, y, w, h, align="left"):
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
        pygame.draw.rect(self.back, (255,0,0), (0,0,w,h))
        self.actualx = panelx + x
        self.actualy = panely + y
    
    def draw(self):
        self.parentSurface.blit(self.back, (self.backx, self.backy))
        self.parentSurface.blit(self.icon, (self.iconx, self.icony))
        
    def testButton(self, mx, my):
        xmin = self.actualx
        xmax = xmin + self.w
        ymin = self.actualy
        ymax = ymin + self.h
        if (mx >= xmin and mx <= xmax) and (my >= ymin and my <= ymax):
            return True


class CartesianGridButton(Button):
    def __init__(self):
        self.icon = pygame.image.load('images/gridIcon.png').convert()        
        
class PolarGridButton(Button):
    def __init__(self):
        self.icon = pygame.image.load('images/polarIcon.png').convert()
        
class SnapToGridButton(Button):
    def __init__(self):
        self.icon = pygame.image.load('images/snapIcon.png').convert()
        
class RunButton(Button):
    def __init__(self):
        self.icon = pygame.image.load('images/runIcon.png').convert()