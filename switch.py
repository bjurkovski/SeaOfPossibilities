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
	def __init__(self, sizeX, sizeY):
		self.id = "Switch" + str(Switch.SwitchID)
		Switch.SwitchID += 1

		Switch.cardMaker.setFrame(-sizeX/2.0, sizeX/2.0, 0, sizeY)

		self.model = NodePath(Switch.cardMaker.generate())

		self.map = None

	def getNode(self):
		return self.model

	def setPos(self, x, y):
		self.model.setPos(x, 0, y)

	def getPos(self):
		return Point2(self.model.getX(), self.model.getZ())

	def setMap(self, _map):
		self.map = _map
