class Body:
	id = 0
	def __init__(self, type_):
		self.type = type_
		self.id = Body.id
		Body.id+= 1

	def getType(self):
		return self.type
		
	def __eq__(self, other):
		return self.id == other.id
