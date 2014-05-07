import serial
import time
import logging
from sys import exit

logging.basicConfig(level=logging.DEBUG, filename="connectiontesting.log", format='%(asctime)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

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
s.write("at sp 0 \r")
s.write("01 0D \r")
s.read(50)

def read(code):
	s.write(code)
	speed_hex = s.read(50).replace('>','').replace('\r', '').replace('\n', '')
	logging.info("Read is " + speed_hex)

logging.info("Testing for speed change...")
for i in xrange(10):
	read("01 0D \r")

s.close()