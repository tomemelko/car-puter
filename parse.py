from datetime import datetime
import time

maxSpeed = 0
maxAccel = 0
destroyCount = 0
startTime = ""
date = ""
totalDist = 0
lastTime = 0
thisTime = 0
lastSpeed = 0
thisSpeed = 0

def trapezoidalDist(t1, t2, s1, s2):
	return ((t2 - t1) / 3600000.0) * ((s1 + s2) / 2)

def acceleration(t1, t2, s1, s2):
	if (t2 - t1) == 0 or (s2 - s1) == 0:
		return 0
	return (((s2 - s1) / 3600.0) / ((t2 - t1) / 1000.0))/.006060606

for line in open("clean1.log"):
	if destroyCount < 3:
		destroyCount += 1
		continue
	if startTime == "":
		startTime = datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S,%f")
	date = datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S,%f")
	
	thisTime = int(time.mktime(date.timetuple()) * 1000 + date.microsecond / 1000)
	thisSpeed = int(line[-4:-1], 16) * .62 #now in decimal mph

	if lastTime == 0 or lastSpeed == 0:
		lastTime = thisTime
		lastSpeed = thisSpeed

	totalDist += trapezoidalDist(lastTime, thisTime, lastSpeed, thisSpeed)
	accel = acceleration(lastTime, thisTime, lastSpeed, thisSpeed)

	if thisSpeed > maxSpeed:
		maxSpeed = thisSpeed

	if accel > maxAccel:
		maxAccel = accel

	lastTime = thisTime
	lastSpeed = thisSpeed

print "Top speed:", maxSpeed,"mph"
print "Elapsed time:", date - startTime
print "Distance traveled:", totalDist,"miles"
print "Peak accel", maxAccel,"g"