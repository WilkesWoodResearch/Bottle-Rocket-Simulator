from math import *
watDensity = 1000 #kg/m^3
airDensity = 1.275 #kg/m^3
gravityInitial = 9.8 #m/s^2
avgRadiusEarth = 6371.0 #km
accuracy = 3 # number of digits

timeStep = float(input("Time step: ")) #seconds
pressure = float(input("pressure (psi): ")) #psi (later converted to Pa)
volume = float(input("Total volume (liters): ")) #liters
iMix = float(input("Percent water: ")) #percent
emptyMass = float(input("Empty weight (kg): ")) #kg
rocketRadius = float(input("Rocket Radius (cm): ")) #cm (later converted to m)
nozzleRadius = float(input("Nozzle radius (cm): ")) #cm (later converted to m)

iMix = iMix/100 #Changing to percent decimal
pressure = pressure*6894.7572931783 #Converting to Pa (N/m^2)
pressureInitial = pressure
volume = volume*1e-3 #Converting to M^3
nozzleRadius = nozzleRadius*1e-2 #Converting to M
rocketRadius = rocketRadius*1e-2 #Converting to M

airvolume = volume*(1-iMix)
airvolumeInitial = airvolume
watVolume = volume*iMix
watVolumeInitial = watVolume

time = 0 #seconds
acc = 0 #m/s^2
maxAcc = 0 #m/s^2
vel = 0 #m/s
pos = 0.0 #m
watVel = 0 #m/s
volumeFlowRate = 0 #m^3/s
massFlowRate = 0 #kg/s
thrustForce = 0 #N
isp = 0 #m/s
maxIsp = 0
avgIsp = 0
airResistance = 0 #N (kg m/s^2)
mass = 0 #kg
gravity = gravityInitial
latentLiftoff = False
latentRecorded = False
latentLiftoffTime = 0
latentLiftoffWatPercentage = 0

loopCount = 0
while 1: #This loop is specifically run only when the rocket is firing
    gravity = (gravityInitial*pow(avgRadiusEarth,2))/float(pow((pos/1000.0)+avgRadiusEarth,2))
    print("Time: "+str(round(time,accuracy))+"s - vel: "+str(round(vel,accuracy))+"m/s - Height: "+str(round(pos*3.281,accuracy))+"ft - Water: "+str(round((watVolume/watVolumeInitial)*100,accuracy))+"%"+" - isp: "+str(round(isp,accuracy)))
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
    isp = thrustForce/massFlowRate
    if(isp>maxIsp):
        maxIsp = isp
    avgIsp += isp
    airResistance = .5*airDensity*pow(vel,2)*pi*pow(rocketRadius,2) #Calculating Air Resistance
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
    loopCount += 1

burnTime = time
maxVel = vel
avgIsp /= loopCount

while(vel>0):
    print("Time: "+str(round(time,accuracy))+"s - vel: "+str(round(vel,accuracy))+"m/s - height: "+str(round(pos*3.281,accuracy))+"ft"+" - gravity: "+str(round(gravity,accuracy)))
    time= time+timeStep
    vel = vel-(gravity*timeStep)
    pos = pos+(vel*timeStep)

print("\n")
if(latentLiftoff and not latentRecorded):
    print("NEVER TOOK OFF")
if(latentLiftoff):
    print("Time till liftoff: "+str(round(burnTime,accuracy))+" seconds\nLiftoff Water Percentage: "+str(round(latentLiftoffWatPercentage,accuracy))+"%")
print("Rocket Height: "+str(round(volume/(pi*pow(rocketRadius,2)),accuracy))+" m")
print("Max isp: " + str(round(maxIsp,accuracy)) + " m/s or " + str(round(maxIsp/9.80665,accuracy)) + " s")
print("Avg isp: " + str(round(avgIsp,accuracy)) + " m/s or " + str(round(avgIsp/9.80665,accuracy)) + " s")
input("Burn time: "+str(round(burnTime,accuracy))+" seconds\nMax G-Force: "+str(round(maxAcc/9.8,accuracy))+" g's\nMax Velocity: "+str(round(maxVel,accuracy))+" m/s ("+str(round(maxVel*2.237,accuracy))+" mph)"+"\nTime to peak: "+str(round(time,accuracy))+" seconds\nPeak Height: "+str(round(pos*3.281,accuracy))+" ft ("+str(round(pos,accuracy))+" m)")
