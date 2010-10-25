import json
from model import *
from direct.actor.Actor import Actor
from panda3d.core import Point3

#class Character(Model):
class Character():
	baseSpeed = 0.05
	def __init__(self, charFile):
		#Model.__init__(self, charFile)
		
		# from model
		file = open(charFile)
		self.data = json.loads(file.read())
		file.close()
		
		self.level = 1
		self.hearts = 6
		self.maxSlots = 1
		self.slots = []
		self.currentSlot = 0
		self.speed = Character.baseSpeed * self.data["speed"]

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])

		self.isMoving = False
		
		# from model
		self.readRenderData()
		
	# from model
	def readRenderData(self):
		self.model.setScale(self.data["render"]["scale"][0], self.data["render"]["scale"][1], self.data["render"]["scale"][2])
		self.model.setHpr(self.data["render"]["hpr"][0], self.data["render"]["hpr"][1], self.data["render"]["hpr"][2])
		self.model.setPos(self.data["render"]["pos"][0], self.data["render"]["pos"][1],self.data["render"]["pos"][2])
	
	# from model
	def getNode(self):
		return self.model
		
	def doAction(self, pressedKeys):
		displacement = Point3(0, 0, 0)
		
		if 'up' in pressedKeys:
			self.model.setHpr(0,0,180)
			displacement += Point3(0, 0, self.speed)
		if 'left' in pressedKeys:
			self.model.setHpr(0,0,90)
			displacement += Point3(-self.speed, 0, 0)
		if 'down' in pressedKeys:
			self.model.setHpr(0,0,0)
			displacement += Point3(0, 0, -self.speed)
		if 'right' in pressedKeys:
			self.model.setHpr(0,0,270)
			displacement += Point3(self.speed, 0, 0)
			
		if displacement[0]!=0 or displacement[1]!=0 or displacement[2]!=0:
			if self.isMoving is False:
				self.model.loop("walk")
				self.isMoving = True
		else:
			if self.isMoving:
				self.model.stop()
				#self.model.pose("walk",5) #transition between run and stop, if actor was looping 'run' animation
				self.isMoving = False

		self.model.setPos(self.model.getPos() + displacement)
		
	def pickItem(self, itemName):
		if len(self.slots) < self.maxSlots:
			self.slots.append(itemName)
		else:
			oldItem = self.slots[self.currentSlot]
			self.slots[self.currentSlot] = itemName
			return oldItem
		

