# Import modules
from screen import Screen
from datacontroller import DataController



# Define global
cartData = {
	"reverse" : False
}


# Methods	

	
	
	
# Setup
datacontroller = DataController()
app = Screen(cartData, datacontroller)




# Run
datacontroller.getData()
app.run()














