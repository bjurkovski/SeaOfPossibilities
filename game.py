from state import *
from stage import *

from direct.actor.Actor import Actor
from panda3d.core import Point3

class Game(State):
	def __init__(self, stage, characters):
		State.__init__(self)

		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.stage = stage
		self.room = self.stage.start

		#test stuff
		self.actor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
		self.actor.setScale(0.0005, 0.0005, 0.0005)
		self.actor.setHpr(0, 90, 0)
		self.actor.loop("walk")
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.render.attachNewNode(self.stage.maps[self.room].getNode())
		self.actor.reparentTo(self.render)
		
	def iterate(self):
		State.iterate(self)
		self.camera.setPos(0, -4, 0)
		self.camera.lookAt(0, 0, 0)
		self.move()
		
		if self.keys['start']:
			return "Paused"

	def move(self):
		disp = Point3(0, 0, 0)
		try:
			if self.keys['up']:
				disp += Point3(0, 0, 0.05)
			if self.keys['left']:
				disp += Point3(-0.05, 0, 0)
			if self.keys['down']:
				disp += Point3(0, 0, -0.05)
			if self.keys['right']:
				disp += Point3(0.05, 0, 0)
		except:
			pass

		self.actor.setPos(self.actor.getPos() + disp)

# to do (or not): create GameServer and GameClient classes to inherit from Game

