# Import modules
from screen import Screen
from datacontroller import DataController
from JSONKeys import JSONKeys
import threading


# Define global
cartData = {
	"reverse" : False,
    JSONKeys.speed.value : 0,
    JSONKeys.temperature.value : 0,
    JSONKeys.voltage.value : 0
}

# Methods	
def beginDataObservation(self):
    pass
	
	
# Setup
datacontroller = DataController()
app = Screen(cartData, datacontroller)




# Run
print(datacontroller.getData())
app.run()














