import java
import sys
import time
from array import *
from math import *
from java.awt import *
import configs.noErrors as cfg
from com.jreitter.philipp.udacity.simulator.abstracts import *
from com.jreitter.philipp.udacity.simulator.view import *
from com.jreitter.philipp.udacity.simulator import *
from com.jreitter.philipp.controller import *
from com.jreitter.philipp.udacity import *
from com.jreitter.philipp.util import *
#IMPORTS 'n STUFF

GOAL = [73, 52]
heuristic = []
FRAME = None
LISTENER = None

def initWorld():
    global heuristic
    h = 138
    w = []
    for i in range(cfg.worldWidth/cfg.worldSpacing):
        col = []
        hcol = []
        h2 = h
        for j in range(cfg.worldHeight/cfg.worldSpacing):
            col.append(0)
            hcol.append(h2)
            h2-=1
        h-=1
        w.append(col)
        heuristic.append(hcol)
    return w
    
def buildMap(w, pos, dots):
    for d in dots:
        x = int((d[0]+pos[0])/cfg.worldSpacing)
        y = int((d[1]+pos[1])/cfg.worldSpacing)
        w[x][y] = 1
    return w
        
def drawMap(w, g):
    g.setColor(Color.red)
    for x in range(cfg.worldWidth/cfg.worldSpacing):
        for y in range(cfg.worldHeight/cfg.worldSpacing):
            if w[x][y] == 1:
                g.drawRect(x*cfg.worldSpacing, y*cfg.worldSpacing, cfg.worldSpacing,cfg.worldSpacing)
        
delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

cost = [1, 1, 1, 1]

def nearWall(x,y,w):
    for dx in range(9):
        for dy in range(9):
            nx = x+dx-4
            ny = y+dy-4
            if x >= 0 and x < len(w) and y >= 0 and y < len(w[0]):
                if w[nx][ny] == 1:
                    return True
    return False
                       
def search(s,w):
    x = int(s[0])
    y = int(s[1])
    
    closed = [[0 for row in range(len(w[0]))] for col in range(len(w))]
    closed[x][y] = 1

    action = [[-1 for row in range(len(w[0]))] for col in range(len(w))]

    g = 0
    f = heuristic[x][y]

    open = [[f, g, x, y]]

    found = False  # flag that is set when search is complet
    resign = False # flag set if we can't find expand
    
    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[2]
            y = next[3]
            g = next[1]
            f = next[0]
            
            if x == GOAL[0] and y == GOAL[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(w) and y2 >=0 and y2 < len(w[0]):
                        if closed[x2][y2] == 0 and nearWall(x2,y2,w) == False:
                            g2 = g + cost[i]
                            f2 = g2 + heuristic[x2][y2]
                            open.append([f2, g2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2] = i
        
    return action

def generatePath(s,r):
    path = []
    x = GOAL[0]
    y = GOAL[1]
    while x != int(s[0]) or y != int(s[1]):
        x2 = x - delta[r[x][y]][0]
        y2 = y - delta[r[x][y]][1]
        path.append([x2,y2])
        x = x2
        y = y2
    return path

def drawPath(g,p):
    w = cfg.worldSpacing
    for a in p:
        g.fillRect(int(a[0]*w),int(a[1]*w),w,w)

def drawLinePath(g,p):
    g.setStroke(BasicStroke(2))
    w = cfg.worldSpacing
    pre = p[0]
    for a in p:
        g.drawLine(int(pre[0]*w), int(pre[1]*w), int(a[0]*w), int(a[1]*w))
        pre = a
    g.setStroke(BasicStroke(1))
        
        
def smooth(path, weight_data = 0.075, weight_smooth = 0.4, tolerance = 0.001):
    
    newpath = [[0 for row in range(len(path[0]))] for col in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]


    change = tolerance
    while change >= tolerance:
        change = 0.0
        
        for i in range(1,len(newpath)-1):
            for j in range(len(newpath[0])):
                aux = newpath[i][j]
                newpath[i][j] += weight_data * ((path[i][j])-newpath[i][j])
                newpath[i][j] += weight_smooth * (newpath[i-1][j] \
                                                  + newpath[i+1][j] - (2.0*newpath[i][j]))                      
                change += abs(aux-newpath[i][j])
                
       # LISTENER.setSPath(newpath)
        #FRAME.repaint()
        
       # time.sleep(change/50)
    
    return newpath 