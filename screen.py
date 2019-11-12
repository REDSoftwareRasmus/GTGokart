# Import modules
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import RPi.GPIO as GPIO


class Screen(object):
	
	# Properties
	
	
    
	# Methods
 
    # MARK: Setup
	def __init__(self, cartData, datacontroller, **kwargs):
		
		# Set 
		self.cartData = cartData
		self.datacontroller = datacontroller
		
        # Define colors
		self.GKRed = '#b80000'
		self.GKGreen = '#4cb359'

        self.sWIDTH =  self.root.winfo_screenwidth()
        self.sHEIGHT = self.root.winfo_screenheight()
        
        self.myFont = tkFont.Font(root = self.root, family = "Helvetica", size = 20, weight = "bold")


		# Instantiate GUI session
		self.root = Tk()

	
    
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
		canvas = Canvas(root, width = self.sWIDTH, height = self.sHEIGHT, bd=0, highlightthickness=0, relief='ridge')
		canvas.pack()
		
		
        #Images
		#pilImage = Image.open('gui-background.jpeg')
		#pilImage = pilImage.resize((self.sWIDTH*2, self.sHEIGHT*2), Image.ANTIALIAS)
		#image = ImageTk.PhotoImage(pilImage)
		
        #Keep image reference in memory
        bg_image = getImage('gui-background.jpeg', self.sWIDTH*2, self.sHEIGHT*2)
        bg_image_CANVAS = canvas.create_image(0, 0, image = bg_image)
		root.bg_image = image
        
		
		#Buttons
		exitButton = Button(self.root, text = "X", font = self.myFont, command = self.__exit, height = 1, width = 1, fg='#ffffff', bg=self.GKRed, activebackground=self.GKRed, highlightthickness=0, bd=0)
		exitButton.place(x=10, y=10)
	
		self.reverseButtonSelection = Button(self.root, text = "Reverse: OFF", font = self.myFont, command = self.reverseButtonPressed, height = 2, width = 14, fg='#ffffff', bg=self.GKRed, activebackground=self.GKRed, highlightthickness=0, bd=0)
		self.reverseButtonSelection.place(x=self.sWIDTH * 0.35, y=10)
		
		
        
    #MARK: GUI Creation
    def getImage(self, name, width, height):
        pilImage = Image.open(name)
        pilImage = pilImage.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        
        return image
  
  
  
	#MARK: Actions
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
		
		import sys
		sys.exit()
	
	
	
	
	
#SIGNAL
	#Back button
	#Motor temperature warning
	#Collision warning

#DATA
	#Velocity label
	#Motor temperature label


