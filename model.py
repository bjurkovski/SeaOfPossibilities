import json
from direct.actor.Actor import Actor
from panda3d.core import Point3

class Model:
	def __init__(self, filename):
		file = open(filename)
		self.data = json.loads(file.read())
		file.close()
		
		#in the case of a normal model still needs to load it
		
		self.readRenderData()
		
	def readRenderData(self):
		self.model.setScale(self.data["render"]["scale"][0], self.data["render"]["scale"][1], self.data["render"]["scale"][2])
		self.model.setHpr(self.data["render"]["hpr"][0], self.data["render"]["hpr"][1], self.data["render"]["hpr"][2])
		self.model.setPos(self.data["render"]["pos"][0], self.data["render"]["pos"][1],self.data["render"]["pos"][2])
	
	def getNode(self):
		return self.model

