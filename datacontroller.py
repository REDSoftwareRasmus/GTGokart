# Import modules
import RPi.GPIO as GPIO
import serial


class DataController():
	
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		
		self.dStream = serial.Serial("/dev/ttyACM0", 9600)
		self.dStream.baudrate = 9600
		
		
	def write(self, PIN, SIGNAL):
		
		# Setup generic pin and output signal
		GPIO.setup(PIN, GPIO.OUT)
		GPIO.output(PIN, SIGNAL)
		
		print(PIN, SIGNAL, "Changed status")
		
		
	def readSerial(self):
		return self.dStream.readline()
		
