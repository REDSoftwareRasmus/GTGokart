# Import modules
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import RPi.GPIO as GPIO
from JSONKeys import JSONKeys


class Screen():
	
	# MARK: Setup
	def __init__(self, cartData, datacontroller, **kwargs):
		
		#Instantiate root session
		self.root = Tk()
		
		# Set 
		self.cartData = cartData
		self.datacontroller = datacontroller
		
        # Define colors
		self.GKRed = '#b80000'
		self.GKGreen = '#4cb359'
		
		self.sWIDTH = self.root.winfo_screenwidth()
		self.sHEIGHT = self.root.winfo_screenheight()
		
		# Set fonts
		self.myFont = tkFont.Font(root = self.root, family = "Beantown", size = 17, weight = "bold")
		self.velFont1 = tkFont.Font(root = self.root, family = "Beantown", size = 60, weight = "bold")
		self.velFont2 = tkFont.Font(root = self.root, family = "Beantown", size = 20)
		self.barFont1 = tkFont.Font(root = self.root, family = "Beantown", size = 17, weight = "bold")
		self.barFont2 = tkFont.Font(root = self.root, family = "Beantown", size = 12, weight = "bold")
		
		#Setup screen
		self.__setupScreen(self.root)
		self.__setupGUI(self.root)
		
    
	def __setupScreen(self, root):
		pad = 3
		self._geom = '200x200+0+0'
		root.geometry("{0}x{1}+0+0".format(
						root.winfo_screenwidth()-pad,
						root.winfo_screenheight()-pad))
						
		root.wm_attributes('-fullscreen', 'true')
	
	def __setupGUI(self, root):
		
		root.title("GTGokart")
		
		#Background canvas
		self.canvas = Canvas(root, width = self.sWIDTH, height = self.sHEIGHT, bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack()
		
		#Add canvas events
		self.canvas.bind('<Button-1>', self.clickEvent)
		
        #Setup static UI
		bg_image = self.getImage("gui-background.jpeg", self.sWIDTH*2, self.sHEIGHT*2)
		self.canvas.create_image(0, 0, image = bg_image)
		root.bg_image = bg_image
		
		velInd_image_1 = self.getImage("gokart-panel-layer-1.png", 480, 500)
		self.canvas.create_image(self.sWIDTH*0.5, self.sHEIGHT*0.73, image=velInd_image_1)
		root.velInd_image_1 = velInd_image_1
		
		self.canvas.create_text(self.sWIDTH*0.5, self.sHEIGHT*0.83, font=self.velFont2, text="km/h", fill='#ffffff')
		
		bar_bg_1 = self.getImage("bar-background.png", 100, 400)
		self.canvas.create_image(self.sWIDTH*0.05, self.sHEIGHT*0.6, image=bar_bg_1)
		root.bar_bg_1 = bar_bg_1
		
		bar_bg_2 = self.getImage("bar-background.png", 100, 400)
		self.canvas.create_image(self.sWIDTH*0.95, self.sHEIGHT*0.6, image=bar_bg_2)
		root.bar_bg_2 = bar_bg_2
		
		radio_icon_image = self.getImage("music-button.png", 60, 60)
		self.radio_icon = self.canvas.create_image(self.sWIDTH-40, 40, image=radio_icon_image)
		self.root.radio_icon = radio_icon_image
		
		#Setup dynamic UI
		velInd_2_image = self.getImage("gokart-panel-layer-2.png", 480, 500, 0)
		self.velInd_2 = self.canvas.create_image(self.sWIDTH*0.5, self.sHEIGHT*0.73, image=velInd_2_image)
		self.root.velInd_2_image = velInd_2_image	
		
		self.velocityLabel = self.canvas.create_text(self.sWIDTH*0.5, self.sHEIGHT*0.7, font=self.velFont1, text="0", fill='#ffffff')
		
		bar_battery = self.getImage("battery-bar.png", 95, 400)
		self.batteryBar = self.canvas.create_image(self.sWIDTH*0.05, self.sHEIGHT*0.6, image=bar_battery)
		self.root.bar_battery = bar_battery
		
		bar_temp = self.getImage("heat-bar.png", 95, 400)
		self.tempBar = self.canvas.create_image(self.sWIDTH*0.95, self.sHEIGHT*0.6, image=bar_temp)
		self.root.bar_temp = bar_temp
		
		self.batteryLabel = self.canvas.create_text(self.sWIDTH*0.05, self.sHEIGHT*0.4, font=self.barFont1, text="100", fill='#ffffff')
		self.tempLabel = self.canvas.create_text(self.sWIDTH*0.95, self.sHEIGHT*0.4, font=self.barFont1, text="0", fill='#ffffff')
		
		self.canvas.create_text(self.sWIDTH*0.05, self.sHEIGHT*0.95, font=self.barFont1, text="%", fill='#ffffff')
		self.canvas.create_text(self.sWIDTH*0.95, self.sHEIGHT*0.95, font=self.barFont2, text="C", fill='#ffffff')
		
		brake_icon_image = self.getImage("brake-indicator-gray.png", 40, 40)
		self.brake_icon = self.canvas.create_image(self.sWIDTH*0.46, self.sHEIGHT*0.95, image=brake_icon_image)
		self.root.brake_icon = brake_icon_image
		
		park_icon_image = self.getImage("park-indicator-gray.png", 40, 40)
		self.park_icon = self.canvas.create_image(self.sWIDTH*0.54, self.sHEIGHT*0.95, image=park_icon_image)
		self.root.park_icon = park_icon_image
		
		#Buttons
		exitButtonImage = self.getImage("close-button.gif", 70, 70)
		self.exitButton = self.canvas.create_image(35, 35, image=exitButtonImage)
		self.root.exitButton = exitButtonImage
		
		reverseButtonImage = self.getImage("rev-button-off.gif", 300, 85)
		self.reverseButton = self.canvas.create_image(self.sWIDTH * 0.5, 50, image=reverseButtonImage)
		self.root.reverseButton = reverseButtonImage
		        
        
	#MARK: GUI Creation
	def getImage(self, name, width, height, rotation=0):
		pilImage = Image.open(name)
		pilImage = pilImage.rotate(rotation)
		pilImage = pilImage.resize((width, height), Image.ANTIALIAS)
		image = ImageTk.PhotoImage(pilImage)
		return image
  
  
  
	#MARK: Actions
	def setDynamicUI(self, cartData):
		
		#Get and calculate data
		txt_temp = str(int(cartData[JSONKeys.temperature.value]))
		txt_battery = str(cartData[JSONKeys.battery.value])
		txt_velocity = str(int(cartData[JSONKeys.velocity.value]))
		velInd_rotation = round((cartData[JSONKeys.velocity.value] / 30.0) * -247)
		
		battery_coors = self.canvas.coords(self.batteryBar)
		temp_coors = self.canvas.coords(self.tempBar)
				
		battery_Y = ((self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.battery.value]/100.0))))-battery_coors[1]
		temp_Y = ((self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.temperature.value]/65.0))))-temp_coors[1]
		
		battery_label_coors = self.canvas.coords(self.batteryLabel) 
		temp_label_coors = self.canvas.coords(self.tempLabel)
		
		battery_Y_label = (((self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.battery.value]/100.0)))) - (self.sHEIGHT * 0.2)) - battery_label_coors[1]
		temp_Y_label = (((self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.temperature.value]/65.0)))) - (self.sHEIGHT * 0.2)) - temp_label_coors[1]
		
		
		#Update canvas elements
		velInd_2_image = self.getImage("gokart-panel-layer-2.png", 480, 500, velInd_rotation)	
		self.canvas.itemconfigure(self.velInd_2, image = velInd_2_image)
		self.root.velInd_2_image = velInd_2_image	
		
		self.canvas.itemconfigure(self.velocityLabel, text=txt_velocity)
		
		self.canvas.move(self.batteryBar, 0, battery_Y)
		self.canvas.move(self.tempBar, 0, temp_Y)
		
		self.canvas.itemconfigure(self.batteryLabel, text=txt_battery)
		self.canvas.itemconfigure(self.tempLabel, text=txt_temp)
		
		self.canvas.move(self.batteryLabel, 0, battery_Y_label)		
		self.canvas.move(self.tempLabel, 0, temp_Y_label)
		
	
	def reverseButtonPressed(self):
		
		self.cartData['reverse'] = not self.cartData['reverse']
		
		isReverse = self.cartData['reverse']
		
		if isReverse:
			reverseButtonImage = self.getImage("rev-button-on.gif", 300, 85)
			self.canvas.itemconfig(self.reverseButton, image=reverseButtonImage)
			self.root.reverseButton = reverseButtonImage
			
			# Set reverse signal HIGH
			self.datacontroller.write(4, GPIO.HIGH)
			
		else:
			reverseButtonImage = self.getImage("rev-button-off.gif", 300, 85)
			self.canvas.itemconfig(self.reverseButton, image=reverseButtonImage)
			self.root.reverseButton = reverseButtonImage
		
			# Set reverse signal LOW
			self.datacontroller.write(4, GPIO.LOW)
		
		#DEBUG/TEST
		#self.cartData[JSONKeys.velocity.value] -= 15
		#self.cartData[JSONKeys.battery.value] -= 40
		#self.cartData[JSONKeys.temperature.value] -= 25
		#self.setDynamicUI(self.cartData)
		
	def openMusicController(self):
		print("Open music controller")
        
	def clickEvent(self, event):
		
		#Click coors
		x = event.x
		y = event.y
		
		#Get click trigger widget frame bounds
		exitButtonBounds = self.canvas.bbox(self.exitButton)
		reverseButtonBounds = self.canvas.bbox(self.reverseButton)
		radioButtonBounds = self.canvas.bbox(self.radio_icon)
		
		#Check click trigger in frame
		if x > exitButtonBounds[0] and x < exitButtonBounds[2] and y > exitButtonBounds[1] and y < exitButtonBounds[3]:
			self.__exit()
			
		
		if x > reverseButtonBounds[0] and x < reverseButtonBounds[2] and y > reverseButtonBounds[1] and y < reverseButtonBounds[3]:
			self.reverseButtonPressed()    
			
			
		if x > radioButtonBounds[0] and x < radioButtonBounds[2] and y > radioButtonBounds[1] and y < radioButtonBounds[3]:
			self.openMusicController()
			
       
	#MARK: Sys actions
	def run(self):	
		self.root.mainloop()
	
	
	def __exit(self):
		print("ACTION: Program exit request")
		
		GPIO.cleanup()
		self.root.quit()
		
		import sys
		sys.exit()
	
	
	
	
	
#SIGNAL
	#Reverse button
	#Motor temperature warning
	
	#Collision warning
	#Manual brake

#DATA
	#Velocity label
	#Motor temperature label
	
	
#RADIO


