# Introduction #

Car-sim was written to visualize and test things, learned at udacity. The project is open source and I’m happy if anyone wants to participate. I am trying to implement sensors and objects every week to be able to test what has been taught at udacity’s class CS373.

## The Simulation ##
The simulated time difference is constant 20ms. While you are able to change the simulation speed with the slider, this will not change the simulated time difference. This allows you to run the simulation at a higher or lower speed.

## Using Jython ##
If you want to use Python to control your car, you have to use Jython. It is a Python interpreter that creates Java executable bytecode, and can therefor interact with my simulation code. The CarSim.jar file needs to be in Jythons classpath.

# Starting a Simulation #
For starting a Simulation the following code can be used.
```
s = Simulation()
s.loadConfig("configs/"+cfg.fileName)
s.setListener(MyListener())
v = SimulationFrame(s)
s.start()
v.setVisible(1)
```

**MyListener** is the name of the Listener class you defined.

The configuration file is parsed by Java.utils.Properties and can also be used as a python file. Thus you can use the configured parameters in your Python code. If you define filename inside your Config you can easily switch between configs by importing a different one wire python.
```
import configs.noErrors as cfg

#Now you can use
print cfg.worldWith #etc in your code
```

# The Config File #
All values are either in Pixel or Radiant.
The following parameters are avaliable:
  * **Sensor Errors** define the variance of a normal distributed error  with a mean of the real value
    * **carSteerSensorError**
    * **carSpeedSensorError** removed in 0.2
    * **carGyroSensorError**
    * **cameraImageNoise** is the probability of a wrong color given back
    * **gpsSensorNoise**

  * **Calculation Errors** every randomUpdateTime (in sec) new random values for Calculation are generated, the values are the variance as percentage of current speed/steer (so it will always go in a straight line)
    * **carSteerError**
    * **carSpeedError**

  * **Car Values** they should be pretty self-explanatory.
    * **carMaxSpeed**
    * **carMaxSteer**
    * **carStartX**
    * **carStartY**

  * **Lag Values** define a fist order Lag for speed and steering changes. If the values are 0 no lag is simulated.
    * **carSteerT**
    * **carSpeedT**

  * **World Settings** worldSpacing defines the size of the grid cells. Width and height should be devidable with no remain by the spacing.
    * **worldSpacing**
    * **worldWidth**
    * **worldHeight**

  * **Sensor Update Rates** define the update rate = 50hz/Update. Integers only.
    * **cameraUpdate**
    * **gpsSensorUpdate**

  * **randomUpdateTime** every randomUpdateTime (in sec) new random values for Calculation are generated


# Interfaces #

## Background ##
The Background interface provides 2 functions for reading the "map" of the world.

`int getColorAt(int x, int y)`
Returns the color of the cell at row: y, and column: x

`int getColorAtPixel(float x, float y)`
Returns the color at the coordinate (x,y) considering the cellSpacing


## Simulation Listener ##
The Simulation Listener is used to receive callbacks from the simulation such as sensor data, and the periodic update.

#### onInit(CarController, Background, startX, startY) ####
The Init method gets called before the simulation is started. It provides a instance of the CarController and Background interface, aswell as the start position of the car.

#### onUpdate(dt) ####
Get called every time the simulation is updated. The time difference is currently fixed 20ms (0.02). The update frequency is by default 50 Hz but can be modified dragging the slider in the GUI. Although this increases the frequency the time difference will still be 20ms, allowing for a speed up or slow down.

#### onCamera(pixel) ####
Gets called every time a camera Image is read (freq. defined in config file). The _pixel_ parameter is a 2d array, but currently only 1 pixel is given back.

#### onGPS(pos) ####
Gets called every time a GPS position is calculated (freq. defined in config file). pos is a 1D int array where `pos[0]=x` and `pos[1]=y`.

#### onPaint(Graphics2D) ####
The onPaint method called every time the simulation is being painted. By default this is every time the simulation gets updated. But the Java VM also calls this method if a repaint is needed (e.g. changing the window size)

### Example ###
This is a example Listener class, simply printing all the data, painting a yellow rect and storing the CarController and Background and start position for later use.

```
class MyListener(SimulationListener):
    car = 0
    bg = 0
    
    x = 0
    y = 0
    
    def init(self, ctrl, sx, sy, background):
        self.car = ctrl
        self.bg = background
        self.x = sx
        self.y = sy

    
    def onUpdate(self, dt):
        print "Update " + str(dt)
        

    def onPaint(self, g):
        g.setColor(Color.yellow)
        g.fillRect(100,100,10,10)
        
    def onGPS(self, pos):
        print "GPS: " + str(pos[0]) + ", " + str(pos[1])
        

    def onCamera(self, img):
        print img[0][0]    

```

## Car Controller ##
The CarContoller interface is used to control the car and get speed, steering and gyro values. Those values are forged by the Sensor Error parameters in the configuration file.

`getSpeed()` returns a float representing speed in pixel/sek

`getSteer()` returns a float representing the change of the cars agle per sek. in radiant

`getGyro()` returns the same as `getSteer()` but forged by a different configuration parameter


`setSpeed(float s)` 1=max speed, 0=stop, -1=reverse

`setSteer(float s)` 1=max steering right, 0=straight, -1=max steering left

# Known Bugs #
  * Very rarely the program will not show anything at startup. I assume this is a synchronization fault. Couldn’t fix it yet, just restart the program if this happens.

  * By integrating the data received wire the CarController interface in python, with no simulated errors, the position can be estimated. This estimation will drift very slowly apart from the real position. I assume this happens due to floating point precision, but takes such a long time that it doesn’t really matter.

# Todo #
  * Do better calculation for the steering. Currently the steering changes the cars angle per unit of time. It is possible to turn your car while standing still. And the gyro and steering values are currently the same. **done, bicycle model in 0.2**

  * Better random speed/steering function, currently it just shakes around at high error values because every 20ms a different speed is calculated. **done in 0.2**

  * Maybe add a random but constant over time offset to the sensor errors because due to the errors beeing normal distributed the sensors are pretty exact over longer time.