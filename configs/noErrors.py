#Filename for easy use
fileName="noErrors.py"

#Variance for return values
carSteerSensorError=0
carSpeedSensorError=0
carGyroSensorError=0

#Variance for calculation
carSteerError=0
carSpeedError=0

#Car Settings
carMaxSpeed=100
carMaxSteer=1
carStartX=400
carStartY=100

#First order Lag, T=0->no Lag
carSteerT=0
carSpeedT=0

#World Settings
worldSpacing=10
worldWidth=800
worldHeight=600

#Variance and for GPS
gpsSensorNoise=0

#Probability of wrong Pixel given back
cameraImageNoise=0

#50/update = freq (int only)
cameraUpdate=10
gpsSensorUpdate=10