from stage import *

from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
	def __init__(self, stage, characters):
		ShowBase.__init__(self)
		# maybe reading from a config file whats the start level...
		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.stage = stage
		self.room = self.stage.start

# to do (or not): create GameServer and GameClient classes to inherit from Game
