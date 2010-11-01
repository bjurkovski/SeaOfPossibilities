import json
from model import *
from direct.actor.Actor import Actor
from panda3d.core import Point3

from direct.gui.OnscreenText import OnscreenText

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
		self.speed = Character.baseSpeed * self.data["speed"]
		self.stop()

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])

		self.isMoving = False
		
		# from model
		self.readRenderData()
		self.calculateDimensions()
		
		self.name = self.data["name"]

	# from model
	def getNode(self):
		return self.model
		
	def stop(self):
		try:
			if self.displacement != Point2(0, 0):
				self.old_displacement = self.displacement
		except:
			print('fuck')

		self.displacement = Point2(0, 0)
		
	def doAction(self, action):
		if action == "walk":
			# if 'up' in param:
				# self.model.setHpr(0,0,180)
				# displacement += Point3(0, 0, self.speed)
			# if 'left' in param:
				# self.model.setHpr(0,0,90)
				# displacement += Point3(-self.speed, 0, 0)
			# if 'down' in param:
				# self.model.setHpr(0,0,0)
				# displacement += Point3(0, 0, -self.speed)
			# if 'right' in param:
				# self.model.setHpr(0,0,270)
				# displacement += Point3(self.speed, 0, 0)
				
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

	def drawStatus(self):
		#should draw character status...
		self.statusString = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.5,-0.95), scale = .07)
		self.statusString.setText("%s 	HP: %s" % (self.name,self.hearts) )
		pass

	def takeDamage(self, damage):
		self.hearts -= damage
		if self.hearts < 0:
			self.hearts = 0
		print "MINHA VIDA:", self.hearts
	
	def  isAlive(self):
		return self.hearts > 0
		

