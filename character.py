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
		self.actor.setPos(self.data["render"]["pos"][0], self.data["render"]["pos"][1], self.data["render"]["pos"][2])
		self.isMoving = False
		
	def doAction(self, pressedKeys):
		displacement = Point3(0, 0, 0)
		
		if 'up' in pressedKeys:
			self.actor.setHpr(0,0,180)
			displacement += Point3(0, 0, self.speed)
		if 'left' in pressedKeys:
			self.actor.setHpr(0,0,90)
			displacement += Point3(-self.speed, 0, 0)
		if 'down' in pressedKeys:
			self.actor.setHpr(0,0,0)
			displacement += Point3(0, 0, -self.speed)
		if 'right' in pressedKeys:
			self.actor.setHpr(0,0,270)
			displacement += Point3(self.speed, 0, 0)
			
		if displacement[0]!=0 or displacement[1]!=0 or displacement[2]!=0:
			if self.isMoving is False:
				self.actor.loop("walk")
				self.isMoving = True
		else:
			if self.isMoving:
				self.actor.stop()
				#self.actor.pose("walk",5) #transition between run and stop, if actor was looping 'run' animation
				self.isMoving = False

		self.actor.setPos(self.actor.getPos() + displacement)
		
	def getNode(self):
		return self.actor

