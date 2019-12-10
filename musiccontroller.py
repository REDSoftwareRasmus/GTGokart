from pygame import mixer



class MusicController:
	
	#Properties
	tracks = ["stilldre", "mario", "chameleon", "kungfu", "allstar", "youdontknowme",
				"everybody", "badandboujee", "hypnotize", "livinonaprayer", 
				"cinema", "turndownforwhat"
				]
		
	trackNames = ["Still Dre - Dr.Dre",
					"Mario Kart Theme",
					"Karma Chameleon - Culture Club",
					"Kung Fu Fighting - Carl Douglas",
					"All Star - Smash Mouth",
					"You Don't Know Me - Matroda",
					"Everybody - Backstreet Boys",
					"Bad and Boujee - Migos",
					"Hypnotize - Biggie Smalls",
					"Livin' on a Prayer - Bon Jovi",
					"Cinema - Skrillex",
					"Turn down for what - DJ Snake",
					
					
					]
		
	trackIndex = 0
	
	
	
	#Methods
	def __init__(self, screen):
		
		#Initialize mixer object
		mixer.init()
		mixer.music.set_volume(1.0)
		
		
	def deinit(self):	
		mixer.quit()
	
	def unload(self):
		#mixer.music.unload()
		pass
	
	def play(self, trackIndex):
		
		#Get song from index
		self.trackIndex = trackIndex
		track = self.tracks[self.trackIndex]
		
		#Load and play new song
		mixer.music.load("Tracks/" + track + ".mp3")
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
	
		
		
		
