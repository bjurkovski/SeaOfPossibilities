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
		
	def enter(self):
		# to do:
		# -> primeira vez que entra num estado, chama o construtor do objeto dele
		#    nas proximas, chama apenas esse metodo enter
		# -> criar um NodePath X vazio pra pendurar todos os elementos de um estado
		#    em vez de pendurar direto no render. Assim, basta dar um X.detachNode()
		#    no exit() e um X.reparentTo(self.render) nesse enter()
		pass
	
	def exit(self):
		pass
		