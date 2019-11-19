# Import modules
from screen import Screen
from datacontroller import DataController
from JSONKeys import JSONKeys
import threading


# Define global
cartData = {
	JSONKeys.reverse.value : False,
    JSONKeys.speed.value : 0,
    JSONKeys.temperature.value : 0,
    JSONKeys.battery.value : 0
}



# Methods	
def observeData( ):
	
	#Get data
	jsonData = datacontroller.getData()
	
	if jsonData == None:
		print("Data request returned None")
		return	
		
    
    #Update data in local cart data
	cartData[JSONKeys.speed.value] = jsonData[JSONKeys.speed.value]
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

