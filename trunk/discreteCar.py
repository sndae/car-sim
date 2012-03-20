import java
import sys
from math import *
from java.awt import *
import configs.noErrors as cfg
import discreteAStar as astar
from com.jreitter.philipp.udacity.simulator.abstracts import *
from com.jreitter.philipp.udacity.simulator.view import *
from com.jreitter.philipp.udacity.simulator import *
from com.jreitter.philipp.controller import *
from com.jreitter.philipp.udacity import *
from com.jreitter.philipp.util import *
#IMPORTS 'n STUFF

def getNearestPath(pos,path):
    w = cfg.worldSpacing
    near = [1000000, 0] #:P
    for i in range(len(path)-1):
        d = sqrt((path[i][0]*w-pos[0])**2+(path[i][1]*w-pos[1])**2)        
        if d < near[0]:
            near = [d, i]
    return near[1]

def CTE(pos, path, i):
    w = cfg.worldSpacing
    dx = (path[i+1][0]-path[i][0])*w
    dy = (path[i+1][1]-path[i][1])*w
    a = atan2(dy,dx)
    dx = path[i+1][0]*w-pos[0]
    dy = path[i+1][1]*w-pos[1]
    a2 = atan2(dy,dx)
    return sin(a-a2)*sqrt((path[i+1][0]*w-pos[0])**2+(path[i+1][1]*w-pos[1])**2)
    
            
class MyListener(SimulationListener):

    def init(self, ctrl, background):
        self.dots = [[0,0]]
        self.scanPos = [0,0]
        self.car = ctrl
        self.world = astar.initWorld()     
        self.path = None 
        self.pathStart = None
        self.n = None

        props = [1.4863248743585946, -0.059127044045704756, 605.7002630377223]

        self.p = P(props[0])
        self.i = I(props[1])
        self.d = D(props[2])
        
    def onUpdate(self, dt):
        if self.path != None:
            pos = self.car.getPos()
            self.n = getNearestPath(pos,self.spath)
            
            error = CTE(pos,self.spath,self.n)
            
            self.p.input(error)
            self.i.input(error)
            self.d.input(error)
            
            self.p.update(dt)
            self.i.update(dt)
            self.d.update(dt)
            
            error  = self.p.value()
            error += self.i.value()
            error += self.d.value()
            
            self.car.setSteer(error)
            self.car.setSpeed(0.5)
    
    def onPaint(self, g):
        astar.drawMap(self.world, g)
        if self.path != None:
            g.setColor(Color.green)
            astar.drawPath(g,self.path)
            g.setColor(Color.blue)
            astar.drawLinePath(g,self.spath)
            
            if self.n != None:
                g.setColor(Color.red)
                g.fillRect(int(self.spath[self.n][0]*10)-3,int(self.spath[self.n][1]*10)-3, 6, 6)
        
    def onGPS(self, pos):
        astar = 1
        
    def onCamera(self, img):
        astar = 1
        
    def onScanner(self, dots):
        self.world = astar.buildMap(self.world, self.car.getPos(), dots)
        if self.path == None:
            self.pathStart = [self.car.getPos()[0]/cfg.worldSpacing,self.car.getPos()[1]/cfg.worldSpacing]
            self.path = astar.generatePath(self.pathStart,astar.search(self.pathStart,self.world))
            self.spath = astar.smooth(self.path)
           
    def setPath(self, p):
        self.path = p
        
    def setSPath(self, p):
        self.spath = p
   
   
   
   
        
listener = MyListener()      
s = Simulation()
s.loadConfig("configs/"+cfg.fileName)
s.setListener(listener)
v = SimulationFrame(s)
astar.FRAME = v
astar.LISTENER = listener
s.start()
v.setVisible(1)