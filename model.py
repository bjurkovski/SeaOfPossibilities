import json
from direct.actor.Actor import Actor
from panda3d.core import Point3
from pandac.PandaModules import CollisionNode, CollisionSphere

class Model:
	id = 0
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
		Model.id += 1
		
	def readRenderData(self):
		self.model.setScale(self.data["render"]["scale"][0], self.data["render"]["scale"][1], self.data["render"]["scale"][2])
		self.model.setHpr(self.data["render"]["hpr"][0], self.data["render"]["hpr"][1], self.data["render"]["hpr"][2])
		self.model.setPos(self.data["render"]["pos"][0], self.data["render"]["pos"][1],self.data["render"]["pos"][2])
	
	def getNode(self):
		return self.model

