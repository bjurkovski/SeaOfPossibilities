from body import *
from direct.actor.Actor import Actor
from panda3d.core import Point3

from direct.gui.OnscreenText import OnscreenText

from body import *

class Character(Body):
	def __init__(self, filename):
		Body.__init__(self, filename, 'Character')
		
		self.level = 1
		self.hearts = 6
		self.maxSlots = 1
		self.slots = []
		self.currentSlot = 0

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])
		self.name = self.data["name"]

		self.stop()
		self.isMoving = False
		
		self.readRenderData()
		self.calculateDimensions()
		
		# initialize character status string
		self.statusString = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.7,-0.85), scale = .08)

		
	def stop(self):
		Body.stop(self)
		self.model.stop()
		#self.model.pose("walk",5) #transition between run and stop, if actor was looping 'run' animation
			
	def getCollisionPos(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		
		try:
			self.turn(angles[direction])
			futPos = Body.getCollisionPos(self, direction)
			self.turn(angles[self.direction])
			return futPos
		except KeyError:
			return self.getPos()
		
	def move(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		
		try:
			self.setDirection(direction)
			if self.isMoving is False:
				self.model.loop("walk")
			Body.move(self, direction)
		except KeyError:
			pass
			
	def setDirection(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180} #colocar no json depois...
		self.turn(angles[direction])
		self.direction = direction
			
	def pickItem(self, itemName):
		if len(self.slots) < self.maxSlots:
			print("Picking this %s" % (itemName) )
			self.slots.append(itemName)
		else:
			oldItem = self.slots[self.currentSlot]
			self.slots[self.currentSlot] = itemName
			return oldItem

	def drawStatus(self):
		#should draw character status...

		self.statusString.setText("%s 	HP: %s\nItens: %s" % (self.name,self.hearts,self.slots) )
		pass

	def takeDamage(self, damage):
		self.hearts -= damage
		if self.hearts < 0:
			self.hearts = 0
		print "MINHA VIDA:", self.hearts
	
	def isAlive(self):
		return self.hearts > 0
		

