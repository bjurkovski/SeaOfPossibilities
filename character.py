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
		self.slots = []
		self.currentSlot = 0

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])
		self.name = self.data["name"]
		self.maxSlots = self.data["slots"]
		
		self.stop()
		self.isMoving = False
		
		self.tryToMove = []
		self.tryToDo = None
		
		self.readRenderData()
		self.calculateDimensions()
		
		
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
		except Exception as e:
			print('Na colisao', e)
			return self.getPos()
		
	def move(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		
		try:
			self.setDirection(direction)
			if self.isMoving is False:
				self.model.loop("walk")
			Body.move(self, direction)
		except Exception as e:
			print('no movimento', e)
			pass
			
	def setDirection(self, direction):
		angles = {"up": 270, "left": 0, "down": 90, "right": 180} 
		#colocar no json depois...

		self.turn(angles[direction])
		self.direction = direction

	def changeSlot(self):
		self.currentSlot += 1
		if self.currentSlot >= len(self.slots):
			self.currentSlot = 0			

	def pickItem(self, itemName):
		if len(self.slots) < self.maxSlots:
			print("Picking this %s" % (itemName) )
			self.slots.append(itemName)
		else:
			oldItem = self.slots[self.currentSlot]
			self.slots[self.currentSlot] = itemName
			return oldItem

	def currentItem(self):
		if len(self.slots) > 1:	
			return self.slots[self.currentSlot]['symbol']
		else:
			return None

	def getStatus(self):
		#should draw character status...
		slots = '[ '
		i = 0

		for s in self.slots:
			if i == self.currentSlot:
				slots += '>'
			else:
				slots += '  ' 

			slots += s['symbol'] + ' '
			i += 1

		slots += ']'

		return "%s 	HP: %s\nItens: %s" % (self.name,self.hearts,slots )

	def takeDamage(self, damage):
		self.hearts -= damage
		if self.hearts < 0:
			self.hearts = 0
		print "MINHA VIDA:", self.hearts
	
	def isAlive(self):
		return self.hearts > 0
		

