import json
from direct.actor.Actor import Actor
from panda3d.core import Point3
from pandac.PandaModules import CollisionNode, CollisionSphere
from body import *

class Model(Body):
	def __init__(self, filename):
		Body.__init__(self, filename, 'Model')
		
		self.model = loader.loadModel(self.data["render"]["model"])
		
		self.readRenderData()
		self.calculateDimensions()
		
	def move(self, direction):
		Body.move(self, direction)
		self.direction = direction