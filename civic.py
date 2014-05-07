import serial
import time
from sys import exit

s = serial.Serial(
	port="COM7",
	baudrate=38400,
	timeout=5
)

if s.isOpen():
	print "Opened serial connection..."

def read(code):
	s.write(code)
	time.sleep(0.5)
	response = s.readline()
	if response == '':
		print "Read timeout"
	else:
		print response

# Let's test if we have a connection and check supported PIDs

read("\x00")
read("\x20")
read("\x40")
read("\x60")
read("\x80")

s.close()