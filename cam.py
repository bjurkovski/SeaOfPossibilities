class Cam():
	def __init__(self, camera):
		self.camera = camera
		self.pos = (0, 0, 0)
		self.lookat = (0, 0, 0)
		self.hpr = (0, 0, 0)
	
	def look(self):
		self.camera.setPos(self.pos)
		self.camera.lookAt(self.lookat)
		self.camera.setHpr(self.hpr)
		
	def setPos(self, x, y=None, z=None):
		if y==None and z==None:
			self.pos = x
		else:
			self.pos = (x, y, z)
		
	def lookAt(self, x, y=None, z=None):
		if y==None and z==None:
			self.lookat = x
		else:
			self.lookat = (x, y, z)
		
	def setHpr(self, h, p=None, r=None):
		if p==None and r==None:
			self.hpr = h
		else:
			self.hpr = (h, p, r)