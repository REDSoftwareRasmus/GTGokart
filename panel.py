# Import modules
from screen import Screen
from datacontroller import DataController
from JSONKeys import JSONKeys
import threading


# Define global
cartData = {
	JSONKeys.reverse.value : False,
    JSONKeys.velocity.value : 28,
    JSONKeys.temperature.value : 45,
    JSONKeys.battery.value : 100
}



# Methods	
def observeData():
	print("mf")
	#Set timer for update
	updateTimer = threading.Timer(1, observeData).start()
	
	#Get data
	jsonData = datacontroller.getData()
	
	if jsonData == None:
		print("Data request returned None")
		return	
		
    #Update data in local cart data
	cartData[JSONKeys.velocity.value] = jsonData[JSONKeys.velocity.value]
	cartData[JSONKeys.battery.value] = jsonData[JSONKeys.battery.value]
	cartData[JSONKeys.temperature.value] = jsonData[JSONKeys.temperature.value]
	
	#Update UI
	app.updateUI(cartData)
    

#Setup
datacontroller = DataController()
updateTimer = threading.Timer(1, observeData)
app = Screen(cartData, datacontroller, updateTimer)


#Run
print(datacontroller.getData()) 
updateTimer.start()
app.run()

