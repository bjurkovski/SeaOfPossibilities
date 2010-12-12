from body import *
from direct.actor.Actor import Actor
from panda3d.core import Point3, ClockObject

from body import *

def opposite(dir):
	op = { 'left' : 'right', 'up' : 'down', 'right' : 'left', 'down' : 'up' }
	return op[dir]

class Character(Body):
	maxHearts = 6
	def __init__(self, filename):
		Body.__init__(self, filename, 'Character')

		self.level = 1
		self.hearts = Character.maxHearts
		self.slots = []
		self.currentSlot = 0
		self.lifting = None

		self.model = Actor(self.data["render"]["model"], self.data["render"]["animation"])
		self.name = self.data["name"]
		self.maxSlots = self.data["slots"]

		self.stop()
		self.isMoving = False

		self.tryToMove = []
		self.tryToDo = None

		self.readRenderData()
		self.calculateDimensions()

		self.clock = None

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

		self.setDirection(direction)
		if self.isMoving is False:
			self.model.loop("walk")
		Body.move(self, direction)

	def setDirection(self, direction):
		Body.setDirection(self, direction)
		angles = {"up": 270, "left": 0, "down": 90, "right": 180}
		#colocar no json depois...

		self.turn(angles[direction])

	def changeSlot(self):
		self.currentSlot += 1
		if self.currentSlot >= len(self.slots):
			self.currentSlot = 0

	def pickItem(self, item):
		if len(self.slots) < self.maxSlots:
			print("Picking this %s" % (item.name) )
			self.slots.append(item)
			return None
		else:
			oldItem = self.slots[self.currentSlot]
			self.slots[self.currentSlot] = item
			return oldItem

	def currentItem(self):
		if len(self.slots) > 1:
			return self.slots[self.currentSlot].name
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

			slots += str(s.name) + ' '
			i += 1

		slots += ']'

		return "%s 	HP: %s\nItens: %s" % (self.name,self.hearts,slots )

	def takeDamage(self, damage):
		pos = self.getPos()

		newdir = opposite(self.direction)

		self.setPos( pos + self.speed[newdir]*5 )

		self.hearts -= damage
		if self.hearts < 0:
			self.hearts = 0

	def isAlive(self):
		return self.hearts > 0

	def enemy_move(self,dir):
		#TODO later we'll subclass enemy and everything will be alright
		if self.clock == None:
			self.clock = ClockObject()
			self.last_step = self.clock.getRealTime()

		if self.clock.getRealTime() - self.last_step > 1:
			self.move(dir)
			self.last_step = self.last_step = self.clock.getRealTime()
		else:
			self.move(self.direction)

	def pick(self, liftable):
		self.lifting = liftable
		liftable.setPos(self.getPos())
		liftable.setHeight(-0.07)

