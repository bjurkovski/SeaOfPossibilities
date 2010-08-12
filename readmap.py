import json

class Map:
	def __init__(self, mapFile):
		file = open(filename)
		self.tiles = []
		for line in file.readlines():
			self.tiles.append([c for c in line if c != '\n'])
		file.close()

	def __str__(self):
		str = ""
		for row in self.tiles:
			for tile in row:
				str += tile
			str += "\n"
		return str

class Stage:
	def __init__(self, stageFile):
		file = open(stageFile)
		self.data = json.loads(file.read())
		self.maps = {}
		for room in self.data["rooms"]:
			self.maps[room] = Map(self.data["rooms"][room]["map"])
		file.close()
		


filename = "stage.txt"

a = Stage(filename)	
