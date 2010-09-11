class Menu:
	def __init__(self):
		self.options = []
		self.keys = None
		self.actions = None
		self.selected = 0
		
	def addOptions(self, options):
		self.options += options
		
	def registerKeys(self, keys, actions):
		self.keys = keys
		# Here we register (func, param) pairs to be called when the corresponding key is active
		self.actions = actions
		
	def previousOpt(self):
		self.selected = (self.selected + len(self.options) - 1)%len(self.options)
		return None
		
	def nextOpt(self):
		self.selected = (self.selected +  1)%len(self.options)
		return None
		
	def iterate(self):
		for k in self.keys.keys():
			try:
				if self.keys[k] and self.actions[k]:
					self.keys[k] = False
					return self.actions[k][0](self.actions[k][1])
			except KeyError:
				pass
		
		return None
