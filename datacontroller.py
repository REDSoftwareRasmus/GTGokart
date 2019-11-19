# Import modules
import RPi.GPIO as GPIO
import serial
from JSONKeys import JSONKeys
import json
import threading


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
		
    
    
	def getData(self):
	
        #Observe data flag
		observeData = True
		
        #Tap in and observe data stream
		while observeData:
			
			#Get data from Serial read
			try:
				data = self.dStream.read_all()
			except AttributeError:
				print("No dStream created since USB port connection could not be established")
				return None
			
			#Extract JSON oject
			fIndex = None
			lIndex = None
			
			for index in range(0,len(data)-1):
				char = data[index]
				
				if char == '{':
					fIndex = index
					continue
				if char == '}' and fIndex != None:
					lIndex = index
					break
				
			if fIndex != None and lIndex != None:
				dataRange = data[fIndex:lIndex+1]
				print(dataRange)
				try: 
					jsonData = json.loads(str(dataRange))
				except ValueError:
					print("No JSON object could be loaded")
					return None
				
				#Interrupt while-loop
				observeData = False
    
                return jsonData
		
