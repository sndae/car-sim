from com.jreitter.philipp.udacity.simulator import DefaultCar
from com.jreitter.philipp.controller import *
from java.util import *
from java.io import *

import path
import discreteCar as astar
from platform import system

def run(car, param,path):
    car.init()
    p = P(param[0])
    i = I(param[1])
    d = D(param[2])
    sume = 0
    for run in range(1377):
        pos = [car.getX(),car.getY()]
        n = astar.getNearestPath(pos,path)
        
        error = astar.CTE(pos,path,n)
        sume += error**2
        
        p.input(error)
        i.input(error)
        d.input(error)
        
        p.update(0.02)
        i.update(0.02)
        d.update(0.02)
        
        error  = p.value()
        error += i.value()
        error += d.value()
        
        car.getController().setSteer(error)
        car.getController().setSpeed(0.5)
        
        car.update(0.02)
    return sume


def twiddle(tol):
    car = DefaultCar()
    props = Properties()
    props.load(FileReader("configs/noErrors.py"))
    car.loadProperties( props )

    p = [0.1, 0.05, 100]
    dp = [0.1, 0.05, 10] 
    min_error = run(car, p, path.track)
    error = 0
    
    while sum(dp) >= tol:
        print [min_error, error, p, dp]
        for i in range(len(p)):
            p[i] += dp[i]
            error = run(car, p, path.track)
            if error < min_error:
                min_error = error
                dp[i] *= 1.1
            else:
                p[i] -= 2.0*dp[i]
                error = run(car, p, path.track)
                if error < min_error:
                    min_error = error
                    dp[i] *= 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
                    
twiddle(0.00001)