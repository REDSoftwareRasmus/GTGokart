from pygame import mixer



class MusicController:
	
	#Properties
	tracks = ["stilldre.mp3",
				"mario.mp3",
				"chameleon.mp3",
				"kungfu.mp3"]
		
	trackNames = ["Still Dre - Dr.Dre",
					"Mario Kart Theme",
					"Karma Chameleon - Culture Club",
					"Kung Fu Fighting - Carl Douglas"]
		
	trackIndex = 0
	
	
	#Methods
	def __init__(self, screen):
		
		#Initialize mixer object
		mixer.init()
		mixer.music.set_volume(1.0)
		
		
	def deinit(self):	
		mixer.quit()
	
	def play(self, trackIndex):
		
		#Get song from index
		self.trackIndex = trackIndex
		track = self.tracks[self.trackIndex]
		
		#Load and play new song
		mixer.music.load(track)
		mixer.music.play()
		
	def pause(self):
		mixer.music.pause()
	
	def unpause(self):
		mixer.music.unpause()
		
	def stop(self):
		mixer.music.stop()
		mixer.music.unload()
		
	def rewind(self):	
		mixer.music.rewind()
		
	def playNext(self):
		self.trackIndex += 1
		
		if trackIndex == len(tracks):
			self.trackIndex = 0
			
		self.play(self.trackIndex)
			
	def playPrev(self):
		
		#Play previous if less than 5s into song, else rewind
		if mixer.music.get_position() > 5000:
			self.rewind()
		else:
			self.trackIndex -= 1
			
			if trackIndex == -1:
				self.trackIndex = len(tracks) - 1
				
			self.play(self.trackIndex)
	
		
		
		
