import json
from panda3d.core import NodePath, CardMaker

class Map:
	def __init__(self, filename=None, size=()):
		self.tiles = []
		self.cards = []
		self.nodePath = None
		if filename != None:
			try:
				file = open(filename)
				for line in file.readlines():
					self.tiles.append([c for c in line if c != '\n'])
				file.close()
			except:
				print "Error creating map: %s not found." % mapFile
				exit()
		elif size != ():
			try:
				for i in range(size[0]):
					self.tiles.append([])
					for j in range(size[1]):
						self.tiles[i].append(' ')
			except:
				print "Error creating map: expecting a size=(width, height)."
				exit()
		else:
			print "Error creating map: please provide either the filename or the size to be allocated."
			exit()

		self.constructModel()

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
				card.setPos(sx/2 + row*sx - 1 , 0, sy/2 + tile*sy - 1)
				#card.setTexture(tex)
				self.cards[row].append(card)

	def getNode(self):
		return self.nodePath.node()

class Stage:
	def __init__(self, stageFile):
		try:
			file = open(stageFile)
			data = json.loads(file.read())
			self.start = data["start"]
			self.maps = {}
			for room in data["rooms"]:
				self.maps[room] = Map(filename=data["rooms"][room]["map"])
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

