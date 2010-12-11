import json
from direct.actor.Actor import Actor
from panda3d.core import Point3
from pandac.PandaModules import CollisionNode, CollisionSphere
from body import *
from gameLoader import *

class Model(Body):
	def __init__(self, filename):
		Body.__init__(self, filename, 'Model')

		self.model = loadModel(self.data["render"]["model"])

		self.readRenderData()
		self.calculateDimensions()

	def __repr__(self):
		return "M"

	def move(self, direction):
		Body.move(self, direction)
		Body.setDirection(self, direction)

