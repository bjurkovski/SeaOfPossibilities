from stage import *
from direct.showbase.ShowBase import ShowBase

from pandac.PandaModules import LineSegs

class Game(ShowBase):
	def __init__(self, stage, characters):
		ShowBase.__init__(self)
		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.stage = stage
		self.room = self.stage.start

		ls = LineSegs()
		ls.setColor(1, 0, 0, 1)
		ls.moveTo(0, 0, 0)
		ls.drawTo(0, 1, 0)

		taskMgr.add(self.idle, "Idle")

	def idle(self, param):
		pass

# to do (or not): create GameServer and GameClient classes to inherit from Game
