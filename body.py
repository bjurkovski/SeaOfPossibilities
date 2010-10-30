class Body:
	id = 0
	def __init__(self, type_):
		self.type = type_
		self.id = Body.id
		Body.id+= 1

	def readRenderData(self):

		try:
			#EPIC REFACTOR! Please look at the diff
			self.model.setScale(*self.data["render"]["scale"])
			self.model.setHpr(*self.data["render"]["hpr"])
			self.model.setPos(*self.data["render"]["pos"])
			self.model.setColor(*self.data["render"]["color"])
		except KeyError:
			print("Using default render data for model")


	def getType(self):
		return self.type
		
	def __eq__(self, other):
		return self.id == other.id
