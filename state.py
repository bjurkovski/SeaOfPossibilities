from panda3d.core import NodePath

class State:
	counter=0
	def __init__(self):
		self.render = None
		self.render2d = None
		self.camera = None
		self.keys = None
		self.node = NodePath("State"+str(State.counter)+"Node")
		self.node2d = NodePath("State"+str(State.counter)+"Node2D")
		State.counter+=1

	def iterate(self):
		pass

	def register(self, render, camera, keys, render2d=None):
		self.render = render
		self.render2d = render2d
		self.camera = camera
		self.keys = keys
		self.enter()

	def enter(self):
		self.node.reparentTo(self.render)

		if self.render2d:
			self.node2d.reparentTo(self.render2d)

	def exit(self):
		self.node.detachNode()
		
		if self.render2d:
			self.node2d.detachNode()
