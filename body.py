import json
from panda3d.core import Point2

class Body:
	id = 0
	baseSpeed = 0.05
	def __init__(self, filename, type):
		file = open(filename)
		self.data = json.loads(file.read())
		file.close()
		
		self.type = type
		self.id = Body.id
		speed = 0
		try: speed = Body.baseSpeed * self.data["speed"]
		except KeyError: pass

		self.direction = "down"
		self.speed = {"up": Point2(0, speed),
					  "left": Point2(-speed, 0),
					  "down": Point2(0, -speed),
					  "right": Point2(speed, 0)}
		self.isMoving = False
		self.displacement = Point2(0,0)
		
		Body.id+= 1
		
	def getNode(self):
		return self.model

	def readRenderData(self):
		try:
			self.setScale(*self.data["render"]["scale"])
			self.setHpr(*self.data["render"]["hpr"])
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
	
	def setHpr(self, H, P, R):
		self.model.setHpr((H,P,R))
		self.calculateDimensions()
		
	def setScale(self, X, Y, Z):
		self.model.setScale(X, Y, Z)
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
		
	def stop(self):
		try:
			if self.displacement != Point2(0, 0):
				self.oldDisplacement = self.displacement
		except:
			pass

		self.isMoving = False
		self.displacement = Point2(0, 0)
		
	def getCollisionPos(self, direction):
		dim = {"up":    Point2(0, self.modelLength/2),
			   "left":  Point2(-self.modelWidth/2, 0),
			   "down":  Point2(0, -self.modelLength/2),
			   "right": Point2(self.modelWidth/2, 0)}
		
		try:
			futPos = Point2(self.getPos() + dim[direction] + self.speed[direction])
			return futPos
		except KeyError:
			return self.getPos()
			
	def move(self, direction):		
		try:
			self.displacement = self.speed[direction]			
			if self.isMoving is False:
				self.isMoving = True
			self.setPos(self.getPos() + self.displacement)
			self.oldDisplacement = self.displacement
			self.displacement = Point2(0,0)
		except KeyError:
			pass
