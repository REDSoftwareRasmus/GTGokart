# Import modules
from screen import Screen
import json
from datacontroller import DataController

# Define global
cartData = {
	"reverse" : False
}



# Methods	
def getData():
	
	observeData = True
	
	while observeData:
		data = datacontroller.readSerial()
		print(data)
		
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
			data = data[fIndex:lIndex]
			jsonData = json.loads(data)
			print json["Speed"]
			observeData = False
	
# Setup
datacontroller = DataController()
app = Screen(cartData, datacontroller)




# Run
getData()
#while True:
#	print(datacontroller.readSerial())

app.run()














