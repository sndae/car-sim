#Filename for easy use
fileName="someErrors.py"

#Variance for return values
carSteerSensorError=0.1
carSpeedSensorError=30
carGyroSensorError=0.1

#Variance for calculation
carSteerError=0.1
carSpeedError=30

#Car Settings
carMaxSpeed=100
carMaxSteer=1
carStartX=400
carStartY=100

#First order Lag, T=0->no Lag
carSteerT=0.5
carSpeedT=0.5

#World Settings
worldSpacing=10
worldWidth=800
worldHeight=600

#Variance for GPS
gpsSensorNoise=25

#Probability of wrong Pixel given back
cameraImageNoise=0.05

#50/update = freq (int only)
cameraUpdate=10
gpsSensorUpdate=10