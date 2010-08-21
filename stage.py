import json

class Map:
	def __init__(self, mapFile=None):
		self.tiles = []
		if mapFile != None:
			try:
				file = open(mapFile)
				for line in file.readlines():
					self.tiles.append([c for c in line if c != '\n'])
				file.close()
			except:
				print "Couldn't open map %s!" % mapFile
				exit()

	def __str__(self):
		str = ""
		for row in self.tiles:
			for tile in row:
				str += tile
			str += "\n"
		return str

	def save(self, filename):
		file = open(filename, 'w')
		file.write(self.__str__())
		file.close()

class Stage:
	def __init__(self, stageFile):
		try:
			file = open(stageFile)
			data = json.loads(file.read())
			self.start = data["start"]
			self.maps = {}
			for room in data["rooms"]:
				self.maps[room] = Map(data["rooms"][room]["map"])
			file.close()
		except:
			print "Couldn't open stage %s!" % stageFile
			exit()

	def __str__(self):
		# to do
		str = 'Start Room: "' + self.start + '"\n\n'
		for room in self.maps:
			str += 'Room "' + room + '"\n'
			str += self.maps[room].__str__()
			str += "\n"
		return str

	def save(self, filename):
		# to do: save each one of the stage's maps...
		file = open(filename, 'w')
		#dump a json file
		#file.write(self.__str__())
		file.close()
