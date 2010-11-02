from panda3d.core import Point2

class Body:
	id = 0
	def __init__(self, type_):
		self.type = type_
		self.id = Body.id
		Body.id+= 1

	def readRenderData(self):
		try:
			#EPIC REFACTOR! Please look at the diff
			self.model.setScale(*self.data["render"]["scale"])
			self.model.setHpr(*self.data["render"]["hpr"])
			self.model.setPos(*self.data["render"]["pos"])
			self.model.setColor(*self.data["render"]["color"])
		except KeyError:
			print("Using default render data for model")
			
	def calculateDimensions(self):
		min, max = self.model.getTightBounds()
		size = max-min
		self.modelWidth = size[0]
		self.modelLength = size[2]
		self.modelHeight = size[1]
		
	def rotateHpr(self, H, P, R):
		h,p,r = self.model.getHpr()
		self.model.setHpr(h+H, p+P, r+R)
		self.calculateDimensions()
	
	def setHpr(self, hpr):
		self.model.setHpr(hpr)
		self.calculateDimensions()
		
	def turn(self, degrees):
		self.model.setP(degrees)
		self.calculateDimensions()

	def setPos(self, pos):
		self.model.setPos(pos[0], self.model.getY(), pos[1])
		
	def setHeight(self, height):
		self.model.setY(height)
		
	def getPos(self):
		return Point2(self.model.getX(), self.model.getZ())
		
	def getHeight(self):
		return self.model.getY()

	def getType(self):
		return self.type
		
	def __eq__(self, other):
		return self.id == other.id
