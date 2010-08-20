class Character:
	def __init__(self, charFile):
		self.level = 1
		file = open(charFile)
		file.close()
