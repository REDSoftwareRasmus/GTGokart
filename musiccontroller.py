from pygame import mixer



class MusicController:
	
	#Properties
	tracks = ["stilldre", "mario", "chameleon", "kungfu", "allstar",
				"everybody", "badandboujee", "hypnotize", "livinonaprayer", 
				"cinema", "turndownforwhat", "loseyourself", "elsonidito",
				"dejavu", "milkshake", "flamingo", "canttouchthis", "compton",
				"lavidaloca", "riverside", "boneless", "tequila", "tokyodrift", 
				"iceicebaby"]
		
	trackNames = ["Still Dre - Dr.Dre",
					"Mario Kart Theme",
					"Karma Chameleon - Culture Club",
					"Kung Fu Fighting - Carl Douglas",
					"All Star - Smash Mouth",
					"Everybody - Backstreet Boys",
					"Bad and Boujee - Migos",
					"Hypnotize - Biggie Smalls",
					"Livin' on a Prayer - Bon Jovi",
					"Cinema - Skrillex",
					"Turn down for what - DJ Snake",
					"Lose Yourself - Eminem",
					"El Sonidito - Hechizeros",
					"Deja Vu - Initial D",
					"Milkshake - Kelis",
					"Flamingo - Kero Kero Bonito",
					"U Can't touch this - MC Hammer",
					"Straight Outta Compton - N.W.A",
					"La Vida Loca - Ricky Martin",
					"Riverside - Sidney Samson",
					"Boneless - Steve Aoki", 
					"Tequila - The Champs",
					"Tokyo Drift - Teriyaki Boys",
					"Ice Ice Baby - Vanilla Ice"]
		
	trackIndex = 0
	
	isPlaying = False
	
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
		
		self.isPlaying = True
		
	def pause(self):
		mixer.music.pause()
		self.isPlaying = False
	
	def unpause(self):
		mixer.music.unpause()
		self.isPlaying = True
		
	def stop(self):
		mixer.music.stop()
		mixer.music.unload()
		self.isPlaying = False
		
	def rewind(self):	
		mixer.music.rewind()
		
	def playNext(self):
		self.trackIndex += 1
		
		if self.trackIndex == len(self.tracks):
			self.trackIndex = 0
			
		self.play(self.trackIndex)
			
	def playPrev(self):
		
		#Play previous if less than 5s into song, else rewind
		if mixer.music.get_pos() > 5000:
			self.rewind()
		else:
			self.trackIndex -= 1
			
			if self.trackIndex == -1:
				self.trackIndex = len(self.tracks) - 1
				
			self.play(self.trackIndex)
	
		
		
		
