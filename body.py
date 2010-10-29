class Body:
	id = 0
	def __init__(self, type_):
		self.type = type_
		self.id = Body.id
		Body.id+= 1

	def readRenderData(self):
		self.model.setScale(self.data["render"]["scale"][0], self.data["render"]["scale"][1], self.data["render"]["scale"][2])
		self.model.setHpr(self.data["render"]["hpr"][0], self.data["render"]["hpr"][1], self.data["render"]["hpr"][2])
		self.model.setPos(self.data["render"]["pos"][0], self.data["render"]["pos"][1],self.data["render"]["pos"][2])
			
		try:
			self.model.setColor(self.data["render"]["color"][0], self.data["render"]["color"][1], self.data["render"]["color"][2])
		except KeyError:
			print("Silly python really wanted you to put color information in this model...")


	def getType(self):
		return self.type
		
	def __eq__(self, other):
		return self.id == other.id
