from pygame import mixer



class MusicController:
	
	def __init__(self, screen):
		
		self.player = mixer.init()






	def play(self, mp3):
		
		self.player.music.load("mario.mp3")
		self.player.music.play()
		
		
		
