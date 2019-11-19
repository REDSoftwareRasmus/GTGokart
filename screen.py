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
	def __init__(self, cartData, datacontroller, updateTimer, **kwargs):
		
		#Instantiate root session
		self.root = Tk()
		
		# Set 
		self.updateTimer = updateTimer
		self.cartData = cartData
		self.datacontroller = datacontroller
		
        # Define colors
		self.GKRed = '#b80000'
		self.GKGreen = '#4cb359'
		
		self.sWIDTH = self.root.winfo_screenwidth()
		self.sHEIGHT = self.root.winfo_screenheight()
		
		self.myFont = tkFont.Font(root = self.root, family = "Beantown", size = 17, weight = "bold")
		self.velFont1 = tkFont.Font(root = self.root, family = "Beantown", size = 60, weight = "bold")
		self.velFont2 = tkFont.Font(root = self.root, family = "Beantown", size = 20)
		self.barFont1 = tkFont.Font(root = self.root, family = "Beantown", size = 17, weight = "bold")
		self.barFont2 = tkFont.Font(root = self.root, family = "Beantown", size = 12, weight = "bold")
    
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
		
		
        #STATIC
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
		
		self.setDynamicUI(self.cartData)
		
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
		
		#Get data
		txt_temp = str(cartData[JSONKeys.temperature.value])
		txt_battery = str(cartData[JSONKeys.battery.value])
		txt_velocity = str(cartData[JSONKeys.velocity.value])
		velInd_rotation = round((cartData[JSONKeys.velocity.value] / 30.0) * -247)
		
		battery_Y = (self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.battery.value]/100.0)))
		temp_Y = (self.sHEIGHT*0.6)*(1+(1-(cartData[JSONKeys.temperature.value]/65.0)))
		
		#Setup dynamic UI
		velInd_image_2 = self.getImage("gokart-panel-layer-2.png", 480, 500, velInd_rotation)
		self.canvas.create_image(self.sWIDTH*0.5, self.sHEIGHT*0.73, image=velInd_image_2)
		self.root.velInd_image_2 = velInd_image_2	
		
		self.canvas.create_text(self.sWIDTH*0.5, self.sHEIGHT*0.7, font=self.velFont1, text=txt_velocity, fill='#ffffff')
		
		bar_battery = self.getImage("battery-bar.png", 95, 400)
		self.canvas.create_image(self.sWIDTH*0.05, battery_Y, image=bar_battery)
		self.root.bar_battery = bar_battery
		
		bar_temp = self.getImage("heat-bar.png", 95, 400)
		self.canvas.create_image(self.sWIDTH*0.95, temp_Y, image=bar_temp)
		self.root.bar_temp = bar_temp
		
		self.canvas.create_text(self.sWIDTH*0.05, battery_Y-(self.sHEIGHT*0.2), font=self.barFont1, text=txt_battery, fill='#ffffff')
		self.canvas.create_text(self.sWIDTH*0.95, temp_Y-(self.sHEIGHT*0.2), font=self.barFont1, text=txt_temp, fill='#ffffff')
		
	
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
		
        
        
	#MARK: Sys actions
	def run(self):
		
		# Run setup
		self.__setupScreen(self.root)
		self.__setupGUI(self.root)
		
		self.root.mainloop()
	
	
	def __exit(self):
		print("ACTION: Program exit request")
		
		GPIO.cleanup()
		self.root.quit()
		self.updateTimer.cancel()
		
		import sys
		sys.exit()
	
	
	
	
	
#SIGNAL
	#Back button
	#Motor temperature warning
	#Collision warning

#DATA
	#Velocity label
	#Motor temperature label


