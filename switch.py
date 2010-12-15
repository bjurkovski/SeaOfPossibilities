import json
from direct.actor.Actor import Actor
from panda3d.core import Point2, Point3
from panda3d.core import NodePath, CardMaker, Texture
from pandac.PandaModules import CollisionNode, CollisionSphere
from body import *
from gameLoader import *

class Switch:
	cardMaker = CardMaker('CardMaker-Switches')
	SwitchID = 0
	def __init__(self, name, sizeX, sizeY, active=False):
		self.id = "Switch" + str(Switch.SwitchID)
		Switch.SwitchID += 1

		Switch.cardMaker.setFrame(-sizeX/2.0, sizeX/2.0, 0, sizeY)
		self.model = NodePath(Switch.cardMaker.generate())

		self.name = name

		self.map = None #maybe this is not necessary... i'll check later

		self.active = None
		if active:
			self.activate()
		else:
			self.deactivate()

	def getNode(self):
		return self.model

	def setPos(self, x, y):
		self.model.setPos(x, 0, y)

	def getPos(self):
		return Point2(self.model.getX(), self.model.getZ())

	def setMap(self, _map):
		self.map = _map

	def activate(self):
		self.active = True
		self.model.setColor(0,1,0)

	def deactivate(self):
		self.active = False
		self.model.setColor(1,0,0)
