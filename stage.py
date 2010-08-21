import json
from panda3d.core import NodePath, CardMaker

class Map:
	def __init__(self, mapFile=None):
		self.tiles = []
		self.cards = []
		self.nodePath = None
		if mapFile != None:
			try:
				file = open(mapFile)
				for line in file.readlines():
					self.tiles.append([c for c in line if c != '\n'])
				file.close()
			except:
				print "Couldn't open map %s!" % mapFile
				exit()

	#def __init__(self, width, height):
	#	self.tiles = []
	#	self.cards = []

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

	def constructModel(self):
		if self.nodePath != None:
			self.nodePath.removeNode()
			self.cards = []

		self.nodePath = NodePath("Map")
		cm = CardMaker('CardMaker')

		for row in range(len(self.tiles)):
			self.cards.append([])
			for tile in range(len(self.tiles[row])):
				sx, sy =  2.0/len(self.tiles) , 2.0/len(self.tiles[row])
				cm.setFrame(sx/2, -sx/2, sy/2, -sy/2)
				cm.setColor(0,0.5,0,1)
				card = self.nodePath.attachNewNode(cm.generate())
				card.setPos(sx/2 + i*sx - 1 , 0, sy/2 + j*sy - 1)
				#card.setTexture(tex)
				self.cards[row].append(card)

	def getNodePath(self):
		return self.nodePath

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
