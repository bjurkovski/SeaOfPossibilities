from stage import *

class Game:
	def __init__(self):
		# maybe reading from a config file whats the start level...
		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = []
		self.stage = None
		self.room = None

# to do (or not): create GameServer and GameClient classes to inherit from Game
