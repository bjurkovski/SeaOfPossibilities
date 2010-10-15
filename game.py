from state import *

from stage import *

from direct.actor.Actor import Actor
from panda3d.core import Point3

class Game(State):
	def __init__(self, stage, characters, player):
		State.__init__(self)

		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.player = player
		self.stage = stage
		self.room = self.stage.start
		
	def getPlayerPos(self):
		self.characters[self.player].actor.getPos()
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())
		for char in self.characters.values():
			char.getNode().reparentTo(self.node)
		
		self.camera.setPos(0, -4, 0)
		self.camera.lookAt(0, 0, 0)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()
		self.move()
		
		print(self.getPlayerPos())
		
		if self.keys['start']:
			return "Paused"

	def move(self):
		pressedKeys = [key for key in self.keys.keys() if self.keys[key]]
		self.characters[self.player].doAction(pressedKeys)

# to do (or not): create GameServer and GameClient classes to inherit from Game

