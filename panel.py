# Import modules
from screen import Screen
from datacontroller import DataController

# Define global
applicationFlags = {
	"reverse" : False
}



# Methods	
	
	
# Setup
datacontroller = DataController()
app = Screen(applicationFlags, datacontroller)




# Run
app.run()














