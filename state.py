class State:
	def __init__(self):
		self.render = None
		self.camera = None
		self.keys = None
	
	def iterate(self):
		pass
		
	def register(self, render, camera, keys):
		self.render = render
		self.camera = camera
		self.keys = keys
		