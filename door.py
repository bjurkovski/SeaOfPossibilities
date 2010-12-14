from model import *

class Door(Model):
	def __init__(self, modelFile, openWith, permanent):
		Model.__init__(self, modelFile)
		self.closed = True
		self.openWith = openWith
		self.permanent = permanent

	def open(self, object):
		if object == self.openWith:
			self.closed = False
			self.getNode().detachNode()
			return True
		return False
