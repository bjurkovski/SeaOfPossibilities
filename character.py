import json
from model import *
from direct.actor.Actor import Actor
from panda3d.core import Point3
from pandac.PandaModules import CollisionNode, CollisionSphere

from body import *

#class Character(Model):
class Character(Body):
	baseSpeed = 0.05
	def __init__(self, charFile):
		#Model.__init__(self, charFile)
		Body.__init__(self, 'Charlie')
		
		# from model
		file = open(charFile)
		self.data = json.loads(file.read())
		file.close()
		
		self.level = 1
		self.hearts = 6
		self.maxSlots = 1
		self.slots = []
		self.currentSlot = 0
		#self.speed = Character.baseSpeed * self.data["speed"]
		speed = Character.baseSpeed * self.data["speed"]
		self.speed = {"up": Point2(0, speed),
					  "left": Point2(-speed, 0),
					  "down": Point2(0, -speed),
					  "right": Point2(speed, 0)}
		self.direction = "down"
		self.stop()

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])
		
		# Collision stuff
		#self.collider = self.model.attachNewNode(CollisionNode('Character' + str(Character.id)))
		#cPos = self.data["collision"]["pos"]
		#self.collider.node().addSolid(CollisionSphere(cPos[0], cPos[1], cPos[2], self.data["collision"]["radius"]))
		#self.collider.show()

		self.isMoving = False
		
		# from model
		self.readRenderData()
		self.calculateDimensions()
			
	# from model
	def getNode(self):
		return self.model
		
	def stop(self):
		try:
			if self.displacement != Point2(0, 0):
				self.oldDisplacement = self.displacement
		except:
			print('fuck')

		self.displacement = Point2(0, 0)
		
	def getSpeed(self, direction):
		#disp = {"up": Point2(0, self.speed),
		#		"left": Point2(-self.speed, 0),
		#		"down": Point2(0, -self.speed),
		#		"right": Point2(self.speed, 0)}
		try:
			return self.speed[direction]
		except KeyError:
			return Point2(0,0)
			
	def getCollisionPos(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		dim = {"up":    Point2(0, self.modelLength/2),
			   "left":  Point2(-self.modelWidth/2, 0),
			   "down":  Point2(0, -self.modelLength/2),
			   "right": Point2(self.modelWidth/2, 0)}
		
		self.turn(angles[direction])
		futPos = Point2(self.getPos() + dim[direction] + self.speed[direction])
		self.turn(angles[self.direction])
		return futPos
		#colocar except key erro aqui... e melhorar
		
	def move(self, direction):
		self.direction = direction
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		self.turn(angles[self.direction])
		self.displacement = self.speed[direction]
		self.doAction("walk")
		#colocar except key erro aqui... e melhorar
		
	def doAction(self, action):
		if action == "walk":	
			if self.displacement[0]!=0 or self.displacement[1]!=0:
				if self.isMoving is False:
					self.model.loop("walk")
					self.isMoving = True
			else:
				if self.isMoving:
					self.model.stop()
					#self.model.pose("walk",5) #transition between run and stop, if actor was looping 'run' animation
					self.isMoving = False

			self.setPos(self.getPos() + self.displacement)
			self.oldDisplacement = self.displacement
			
	def pickItem(self, itemName):
		if len(self.slots) < self.maxSlots:
			self.slots.append(itemName)
		else:
			oldItem = self.slots[self.currentSlot]
			self.slots[self.currentSlot] = itemName
			return oldItem
	
	def takeDamage(self, damage):
		self.hearts -= damage
		if self.hearts < 0:
			self.hearts = 0
		print "MINHA VIDA:", self.hearts
	
	def isAlive(self):
		return self.hearts > 0
		

