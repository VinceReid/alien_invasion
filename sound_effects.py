import pygame
from pygame import mixer

class SoundEffects:
	"""defining the sounds to be played"""

	def __init__(self):
		
		self.music_on = 1
		self.game_music()
		self.combo_list = []

		self.bullet = "laser.wav"

	def check_combo(self, event_key):
		"""Check key combo for match"""
		self.combo_list.append(event_key)
		if self.combo_list[-4:] == [102, 97, 114, 116]:
			self.bullet = "fart.wav"
		elif self.combo_list[-5:] == [97, 115, 101, 114, 13]:
			self.bullet = "laser.wav"

	def music_paused(self):
		if self.music_on == 1:
			pygame.mixer.music.unpause()
		elif self.music_on == -1:
			pygame.mixer.music.pause()

	def game_music(self):
		"""background music"""
		pygame.mixer.music.load('arcadeloop.wav')
		pygame.mixer.music.play(-1)

	def crash_sound(self):
		"""Plays the crash sound when an alien colides with ship"""
		crash_sound = pygame.mixer.Sound("lose.wav")
		crash_sound.play()

	def bullet_sound(self):
		"""Plays the bullet sound when bullets are fired"""
		bullet_sound = pygame.mixer.Sound(self.bullet)
		bullet_sound.play()

	def alien_hit_sound(self):
		"""Plays when a bullets hits an alien"""
		alien_hit_sound = pygame.mixer.Sound("alien_hit.wav")
		alien_hit_sound.play()

	def levelup_sound(self):
		"""interups game_music to play level up sound"""
		pygame.mixer.music.pause()
		levelup_sound = pygame.mixer.Sound("levelup.wav")	
		levelup_voice_sound = pygame.mixer.Sound("level-up-voice.wav")	
		levelup_sound.play()
		levelup_voice_sound.play()
		pygame.mixer.music.unpause()

	def game_over_sound(self):
		"""Plays the crash sound when an alien colides with ship"""
		game_over_sound = pygame.mixer.Sound("aliens_game_over2.wav")
		game_over_sound.play()
	

