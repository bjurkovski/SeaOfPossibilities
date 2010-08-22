from stage import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import Point3

class Game(ShowBase):
	def __init__(self, stage, characters):
		ShowBase.__init__(self)
		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.stage = stage
		self.room = self.stage.start

		self.render.attachNewNode(self.stage.maps[self.room].getNode())
		#test stuff
		self.actor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
		self.actor.setScale(0.0005, 0.0005, 0.0005)
		self.actor.setHpr(0, 90, 0)
		self.actor.reparentTo(self.render)
		self.actor.loop("walk")

		#just testing movement
		self.keys = {'w': False, 'a': False, 's': False, 'd': False}
		self.accept('w', self.setKey, ['w', True])
		self.accept('w-up', self.setKey, ['w', False])
		self.accept('a', self.setKey, ['a', True])
		self.accept('a-up', self.setKey, ['a', False])
		self.accept('s', self.setKey, ['s', True])
		self.accept('s-up', self.setKey, ['s', False])
		self.accept('d', self.setKey, ['d', True])
		self.accept('d-up', self.setKey, ['d', False])

		taskMgr.add(self.idle, "Idle")
		taskMgr.add(self.move, "Move")

	#movement test:
	def setKey(self, key, value):
		self.keys[key] = value

	def move(self, param):
		disp = Point3(0, 0, 0)
		if self.keys['w']:
			disp += Point3(0, 0, 0.05)
		if self.keys['a']:
			disp += Point3(-0.05, 0, 0)
		if self.keys['s']:
			disp += Point3(0, 0, -0.05)
		if self.keys['d']:
			disp += Point3(0.05, 0, 0)

		self.actor.setPos(self.actor.getPos() + disp)
		return Task.cont

	def idle(self, param):
		self.camera.setPos(0, -4, 0)
		self.camera.lookAt(0, 0, 0)

		return Task.cont

# to do (or not): create GameServer and GameClient classes to inherit from Game
