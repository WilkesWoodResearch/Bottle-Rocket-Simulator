from math import *
watDensity = 1000 #kg/m^3
airDensity = 1.275 #kg/m^3
gravity = 9.8 #m/s^2
accuracy = 3 # number of digits

timeStep = float(input("Time step: "))
pressure = float(input("pressure (psi): "))
volume = float(input("Total volume (liters): "))
iMix = float(input("Percent water: "))
emptyMass = float(input("Empty weight (kg): "))
rocketRadius = float(input("Rocket Radius (cm): "))
nozzleRadius = float(input("Nozzle radius (cm): "))

iMix = iMix/100 #Changing to percent decimal
pressure = pressure*6895 #Converting to Pa
pressureInitial = pressure
volume = volume*1e-3 #Converting to M^3
nozzleRadius = nozzleRadius*1e-2 #Converting to M
rocketRadius = rocketRadius*1e-2 #Converting to M

airvolume = volume*(1-iMix)
airvolumeInitial = airvolume
watVolume = volume*iMix
watVolumeInitial = watVolume

time = 0
acc = 0
maxAcc = 0
vel = 0
pos = 0
watVel = 0
volumeFlowRate = 0
massFlowRate = 0
thrustForce = 0
airResistance = 0
weight = 0
mass = 0
latentLiftoff = False
latentRecorded = False
latentLiftoffTime = 0
latentLiftoffWatPercentage = 0
while 1:
    print("Time: "+str(round(time,accuracy))+"s - vel: "+str(round(vel,accuracy))+"m/s - Height: "+str(round(pos*3.281,accuracy))+"ft - Water: "+str(round((watVolume/watVolumeInitial)*100,accuracy))+"%")
    time = time+timeStep
    watVel = sqrt((2*pressure)/watDensity)
    volumeFlowRate = pi*pow(nozzleRadius,2)*watVel
    massFlowRate = volumeFlowRate*watDensity
    watVolume = watVolume-(volumeFlowRate*timeStep)
    if(watVolume<0):
        break
    airvolume = airvolume+(volumeFlowRate*timeStep)
    pressure = (pressureInitial*airvolumeInitial)/airvolume
    thrustForce = pi*pow(nozzleRadius,2)*pressure
    airResistance = .5*airDensity*pow(vel,2)*pi*pow(rocketRadius,2)
    mass = emptyMass+(watVolume*watDensity)
    acc = (thrustForce-(mass*gravity)-airResistance)/mass
    if(acc>maxAcc):
        maxAcc=acc
    vel = vel+(acc*timeStep)
    if(vel<0):
        vel=0
        latentLiftoff= True
    else:
        if(latentLiftoff and not latentRecorded):
            latentLiftoffTime = time
            latentLiftoffWatPercentage = (watVolume/watVolumeInitial)*100
            latentRecorded = True
    pos = pos+(vel*timeStep)

burnTime = time
maxVel = vel

while(vel>0):
    print("Time: "+str(round(time,accuracy))+"s - vel: "+str(round(vel,accuracy))+"m/s - height: "+str(round(pos*3.281,accuracy))+"ft")
    time= time+timeStep
    vel = vel-(gravity*timeStep)
    pos = pos+(vel*timeStep)

print("\n")
if(latentLiftoff and not latentRecorded):
    print("NEVER TOOK OFF")
if(latentLiftoff):
    print("Time till liftoff: "+str(round(burnTime,accuracy))+" seconds\nLiftoff Water Percentage: "+str(round(latentLiftoffWatPercentage,accuracy))+"%")
print("Rocket Height: "+str(round(volume/(pi*pow(rocketRadius,2)),accuracy))+" m")
input("Burn time: "+str(round(burnTime,accuracy))+" seconds\nMax G-Force: "+str(round(maxAcc/9.8,accuracy))+" g's\nMax Velocity: "+str(round(maxVel,accuracy))+" m/s ("+str(round(maxVel*2.237,accuracy))+" mph)"+"\nTime to peak: "+str(round(time,accuracy))+" seconds\nPeak Height: "+str(round(pos*3.281,accuracy))+" ft")
