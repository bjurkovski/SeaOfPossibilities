from panda3d.core import NodePath

class State:
	counter=0
	def __init__(self):
		self.render = None
		self.camera = None
		self.keys = None
		self.node = NodePath("State"+str(State.counter)+"Node")
		State.counter+=1

	def iterate(self):
		pass

	def register(self, render, camera, keys):
		self.render = render
		self.camera = camera
		self.keys = keys
		self.enter()

	def enter(self):
		self.node.reparentTo(self.render)

	def exit(self):
		self.node.detachNode()

