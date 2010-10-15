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

	def currentMap(self):
		return self.stage.maps[self.room]

	def changeMap(self,direction):
		NodePath(self.currentMap().getNode()).detachNode()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(render)
		self.characters[self.player].getNode().setZ(-0.8)
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())
		for char in self.characters.values():
			char.getNode().reparentTo(self.node)
		
		self.camera.setPos(0, -3, -3)
		self.camera.lookAt(0, 0, 0)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()
		self.camera.camera.setPos(0, -3, -3)
		self.camera.camera.lookAt(0, 0, 0)
		self.move()
		
		if self.keys['start']:
			return "Paused"

	def move(self):
		pressedKeys = [key for key in self.keys.keys() if self.keys[key]]
		self.characters[self.player].doAction(pressedKeys)
		
		sizeX = len(self.stage.maps[self.room].tiles)
		sizeY = len(self.stage.maps[self.room].tiles[0])
		x = int((self.characters[self.player].actor.getX() / (2.0/sizeX)) + sizeX/2)
		y = int((self.characters[self.player].actor.getZ() / (2.0/sizeY)) + sizeY/2)
		ex = self.stage.maps[self.room].getExit((x,y))
		
		print x,y,ex
		if ex and (ex in self.stage.doors[self.room].keys()):
			self.changeMap(ex)

			

# to do (or not): create GameServer and GameClient classes to inherit from Game

