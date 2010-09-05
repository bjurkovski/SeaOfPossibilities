"""
	class Input
	receives keyboard input and returns abstract action strings
	denoting what this input means
	
	Just inherit from this guy and feel the delights of semantic keypresses
""" 
class Input():

	def __init__(self):
		#a mapping of key -> action that denotes which key is binded to which action
		self.keymap = {}
		
		#a mapping of action -> bool, that represents if an action has been requested or not
		self.actionKeys = {}
		
	def inputMap(self,adict):
		#maybe clear old keymap
		for action,key in adict.iteritems():
			self.mapKey(action,key)
			self.actionKeys[self.keymap[key]] = False
	
	def mapKey(self, action, key):
		"""
			Maps a semantic string denoting an action to
			the raw string denoting the key that is pressed for
			this action, an example would be mapKey("jump","space")
		"""
		self.keymap[key] = action
		
	def setKey(self, key, pressed):
		self.actionKeys[self.keymap[key]] = pressed
		
	def bindKeys(self):
		"""
			Binds the current key configuration for one object
		"""
		for k in self.keymap.keys():
			self.accept(k, self.setKey, [k, True])
			self.accept(k + '-up', self.setKey, [k, False])

	def unbindKeys(self):
		"""
			Unbinds the current key configuration
		"""
		#stop receiveing events from these keys
		pass


