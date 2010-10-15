from panda3d.core import Point3

class Cam():
	def __init__(self, camera):
		self.camera = camera
		self.pos = Point3(0, 0, 0)
		self.lookat = Point3(0, 0, 0)
		self.hpr = Point3(0, 0, 0)
	
	def look(self):
		self.camera.setHpr(self.hpr.getX(), self.hpr.getY(), self.hpr.getZ())
		self.camera.lookAt(self.lookat.getX(), self.lookat.getY(), self.lookat.getZ())
		self.camera.setPos(self.pos.getX(), self.pos.getY(), self.pos.getZ())
		
		
	def setPos(self, x, y=None, z=None):
		if y==None and z==None:
			self.pos = x
		else:
			self.pos = Point3(x, y, z)
		
	def lookAt(self, x, y=None, z=None):
		if y==None and z==None:
			self.lookat = x
		else:
			self.lookat = Point3(x, y, z)
		
	def setHpr(self, h, p=None, r=None):
		if p==None and r==None:
			self.hpr = h
		else:
			self.hpr = Point3(h, p, r)