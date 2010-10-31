import json
from direct.actor.Actor import Actor
from panda3d.core import Point3
from pandac.PandaModules import CollisionNode, CollisionSphere
from body import *

class Model(Body):
	def __init__(self, filename):
		file = open(filename)
		self.data = json.loads(file.read())
		file.close()
		
		# maybe we need to include a package to use this function
		self.model = loader.loadModel(self.data["render"]["model"])
		
		# Collision stuff
		#self.collider = self.model.attachNewNode(CollisionNode('Model' + str(Model.id)))
		#cPos = self.data["collision"]["pos"]
		#self.collider.node().addSolid(CollisionSphere(cPos[0], cPos[1], cPos[2], self.data["collision"]["radius"]))
		#self.collider.show()
		
		self.readRenderData()
		self.calculateDimensions()
		
	def getNode(self):
		return self.model
