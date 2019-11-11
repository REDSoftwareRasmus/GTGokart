# Import modules
import RPi.GPIO as GPIO
import serial


class DataController():
	
	def __init__(self):
		
		# Set GPIO pin numbering mode
		GPIO.setmode(GPIO.BCM)
		
		# Setup Datastream from Arduino at ACM0 USB port
		try: 
			self.dStream = serial.Serial("/dev/ttyACM0", 9600)
			self.dStream.baudrate = 9600
		except:
			print("Could not establish connection to USB port ACM0")
			
	def write(self, PIN, SIGNAL):
		
		# Setup generic pin and output signal
		GPIO.setup(PIN, GPIO.OUT)
		GPIO.output(PIN, SIGNAL)
		
		print(PIN, SIGNAL, "Changed status")
		
		
	def readSerial(self):
		return self.dStream.read_all()
		
