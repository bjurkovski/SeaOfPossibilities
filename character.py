import json
from direct.actor.Actor import Actor
from panda3d.core import Point3

class Character:
	baseSpeed = 0.05
	def __init__(self, charFile):
		file = open(charFile)
		self.data = json.loads(file.read())
		file.close()
		
		self.level = 1
		self.hearts = 6
		self.maxSlots = 1
		self.slots = []
		self.speed = Character.baseSpeed * self.data["speed"]

		self.actor = Actor(self.data["render"]["model"], self.data["render"]["animation"])
		self.actor.setScale(self.data["render"]["scale"][0], self.data["render"]["scale"][1], self.data["render"]["scale"][2])
		self.actor.setHpr(self.data["render"]["hpr"][0], self.data["render"]["hpr"][1], self.data["render"]["hpr"][2])
		self.actor.loop("walk")
		
	def doAction(self, pressedKeys):
		displacement = Point3(0, 0, 0)
		
		if 'up' in pressedKeys:
			displacement += Point3(0, 0, self.speed)
		if 'left' in pressedKeys:
			displacement += Point3(-self.speed, 0, 0)
		if 'down' in pressedKeys:
			displacement += Point3(0, 0, -self.speed)
		if 'right' in pressedKeys:
			displacement += Point3(self.speed, 0, 0)
			
		self.actor.setPos(self.actor.getPos() + displacement)
		
	def getNode(self):
		return self.actor