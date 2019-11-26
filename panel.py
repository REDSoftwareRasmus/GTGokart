# Import modules
from screen import Screen
from datacontroller import DataController
from JSONKeys import JSONKeys
import threading
import time


# Define global
cartData = {
	JSONKeys.reverse.value : False,
    JSONKeys.velocity.value : 12,
    JSONKeys.temperature.value : 45,
    JSONKeys.battery.value : 100
}



# Methods	
def bootup():
	for x in range(1,11):
		print "...",
		print str(x*10),
		print "%"
		time.sleep(0.1)


def observeData():
	
	#Set timer for data observation update
	updateTimer = threading.Timer(1, observeData)
	updateTimer.setDaemon(True) #Set to daemon in order to kill this thread when main thread is exited
	updateTimer.start()
	
	#Get data
	jsonData = datacontroller.getData()
	
	if jsonData == None:
		print("Data request returned None")
		updateTimer.cancel()
		return	
		
    #Update data in local cart data
	cartData[JSONKeys.velocity.value] = jsonData[JSONKeys.velocity.value]
	cartData[JSONKeys.battery.value] = jsonData[JSONKeys.battery.value]
	cartData[JSONKeys.temperature.value] = jsonData[JSONKeys.temperature.value]
	
	#Update UI
	app.setDynamicUI(cartData)
    

#Setup
print("Booting up...")
datacontroller = DataController()
app = Screen(cartData, datacontroller)


#Run
observeData()
bootup()
app.run()

