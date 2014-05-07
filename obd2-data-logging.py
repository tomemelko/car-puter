import serial
import time
import logging
from sys import exit
from datetime import datetime

nPolls = 10000000
filename = "run0.log"

#for x in xrange(1,10):
#	path = "run" + str(x) + ".log"
#	if not file.exists(path):
#B		filename = path

logging.basicConfig(level=logging.DEBUG, filename=filename, format='%(asctime)s %(message)s')
epochTime = int(time.mktime(datetime.now().timetuple()) * 1000 + datetime.now().microsecond / 1000)
#logging.getLogger().addHandler(logging.StreamHandler())

s = serial.Serial(
	port="COM7",
	baudrate=38400,
	timeout=.05
	#8databits, no parity, one stop
)

if s.isOpen():
	logging.info("Opened serial connection...")

#autoconfig the device
s.write("at z")
time.sleep(1)
s.write("at sp 0 \r")
time.sleep(1)
s.read(50)

def read(code):
	s.write(code)
	hexData = s.read(50).replace('>','').replace('\r', '').replace('\n', '')
	return hexData

# Time is in ms. Speed in mph
def trapezoidalDist(t1, t2, s1, s2):
	return ((t2 - t1) / 3600000.0) * ((s1 + s2) / 2)

# Time is in ms. Speed in mph
def acceleration(t1, t2, s1, s2):
	if (t2 - t1) == 0 or (s2 - s1) == 0:
		return 0
	return (((s2 - s1) / 3600.0) / ((t2 - t1) / 1000.0))/.006060606

def getSpeed():
	line = read("01 0D \r")
	speed = int(line[-4:-1], 16) * .62 #now in decimal mph
	return speed

def getRPM():
	line = read("01 0C \r")
	if "41 0C" not in line:
		return -1
	bytes = line[line.index("41 0C")+6:-1].split(' ')
	a = int(bytes[0], 16)
	b = int(bytes[1], 16)
	revs = ((a*256)+b)/4
	return revs

def getThrottlePos():
	line = read("01 11 \r")
	if "41 11" not in line:
		return -1
	bytes = line[line.index("41 11") + 6:-1]
	a = int(bytes[0], 16)
	throttle = ((a*100.0)/255)
	return throttle

def getIntakeAirTemp():
	return read("01 0F \r")

def now():
	return int(time.mktime(datetime.now().timetuple()) * 1000 + datetime.now().microsecond / 1000) - epochTime

print "skoskoko"
distance = 0
lastSpeed = 0

logging.warning("Timing " + str(nPolls) + " polls")
startTime = now()
lastTime = startTime
csv = open("data_0_60.csv", 'w')
csv.write("Time,Speed,RPM,Throttle Position\n")
for pollNumber in xrange(nPolls):
	thisTime = now()
	thisSpeed = getSpeed()
	thisRPM = getRPM()
	thisThrottle = getThrottlePos()

	#if thisSpeed == 0 and lastSpeed == 0:
	#	continue

	#do some math
	distance += trapezoidalDist(lastTime, thisTime, lastSpeed, thisSpeed)
	accel = acceleration(lastTime, thisTime, lastSpeed, thisSpeed)

	#csv.write(','.join([thisTime, thisSpeed, thisRPM, thisThrottle]) + "\r\n")
	csv.write(','.join([str(thisTime), str(thisSpeed), str(thisRPM), str(thisThrottle)]) + "\n")

	lastTime = thisTime
	lastSpeed = thisSpeed

elapsedTime = (now() - startTime)

logging.info("Time taken to do " + str(nPolls) + " polls: " + str(elapsedTime/1000) + " seconds")
logging.info("Traveled " + str(distance) + "km")

csv.close()
s.close()
print "I staph nao"