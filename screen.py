# Import modules
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import RPi.GPIO as GPIO
from JSONKeys import JSONKeys


class Screen():
	
	# Properties



	# Methods

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
		
		
		#Buttons
		exitButton = Button(self.root, text = "X", font = self.myFont, command = self.__exit, height = 1, width = 1, fg='#ffffff', bg=self.GKRed, activebackground=self.GKRed, highlightthickness=0, bd=0)
		exitButton.place(x=10, y=10)
		
		self.reverseButtonSelection = Button(self.root, text = "Reverse: OFF", font = self.myFont, command = self.reverseButtonPressed, height = 2, width = 14, fg='#ffffff', bg=self.GKRed, activebackground=self.GKRed, highlightthickness=0, bd=0)
		self.reverseButtonSelection.place(x=self.sWIDTH * 0.35, y=10)
        
        
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
			self.reverseButtonSelection.config(bg = self.GKGreen)
			self.reverseButtonSelection.config(activebackground = self.GKGreen)
			self.reverseButtonSelection.config(text = 'Reverse: ON')
			
			# Set reverse signal HIGH
			self.datacontroller.write(4, GPIO.HIGH)
			
		else:
			self.reverseButtonSelection.config(bg = self.GKRed)
			self.reverseButtonSelection.config(activebackground = self.GKRed)
			self.reverseButtonSelection.config(text = 'Reverse: OFF')
		
			# Set reverse signal LOW
			self.datacontroller.write(4, GPIO.LOW)
		
		#DEBUG/TEST
		#self.cartData[JSONKeys.velocity.value] -= 15
		#self.cartData[JSONKeys.battery.value] -= 40
		#self.cartData[JSONKeys.temperature.value] -= 25
		#self.setDynamicUI(self.cartData)
        
        
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
	#Back button
	#Motor temperature warning
	#Collision warning

#DATA
	#Velocity label
	#Motor temperature label


