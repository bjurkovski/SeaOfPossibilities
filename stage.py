import json
from panda3d.core import NodePath, CardMaker, Texture
from direct.actor.Actor import Actor

tex = Texture('tex')
tex.load('tex/grass.png')

class Map:
	def __init__(self, filename=None, size=()):
		self.tiles = []
		self.cards = []
		self.nodePath = None

		self.readConfig()

		if filename != None:
			try:
				file = open(filename)
				self.tiles = file.read().split()
#				for line in file.readlines():
#					self.tiles.append([c for c in line if c != '\n'])
#				file.close()
			except:
				print "Error creating map: %s not found." % filename
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

		self.width, self.height = len(self.tiles), len(self.tiles[0])

		self.constructModel()

		print(self)

	def readConfig(self):

		cfg = open("cfg/stage.cfg")	
		
		data = json.loads(cfg.read())
		self.tilemap = data['tilemap']
		
		cfg.close()

	def tileIs(self, point , tilename):
		return tilename == self.tilemap[self.tiles[int(point[0])][int(point[1])]]


	def getExit(self,point):
		"""
			Returns a string representing the direction if the given point
			is an exit and None if it's not. 

		"""
		direc = None
		clear = self.tileIs(point, 'ground')
		
		minX = 0
		maxX = len(self.tiles)-1
		minY = 0 
		maxY = len(self.tiles[0])-1
		
		print clear, maxX, maxY
		# in the first line
		if point[1] == maxY and clear:
			return "up"
		# in the last line
		if point[1] == 0 and clear:
			return "down"
		if point[0] == 0 and clear:
			return "left"
		if point[0] == maxX and clear:
			return "right"
		
		return direc

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

		for i in range(len(self.tiles)):
			self.cards.append([])
			for j in range(len(self.tiles[i])):
				sx, sy =  2.0/len(self.tiles) , 2.0/len(self.tiles[i])
				cm.setFrame(sx/2, -sx/2, sy/2, -sy/2)
				#cm.setColor(1,1,1,1)
				card = self.nodePath.attachNewNode(cm.generate())
				card.setPos((sx/2 + i*sx - 1 ), 0,(sy/2 + j*sy - 1))
				
				card.setTexture(tex)
				
				self.cards[i].append(card)
				card.reparentTo(self.nodePath)
				
				if self.tileIs( (i,j), 'obstacle'):
					m =	 Actor('model/rock/rock') 
					m.reparentTo(card)
					m.setHpr(0,90,0)
					m.setPos(m.getPos() - (sx/10, -0.08, sy/2))
					m.setScale(0.012,0.012,0.012)
					#self.cards[i][j].setColor(1,0,0)

	def getNode(self):
		return self.nodePath.node()

class Stage:
	def __init__(self, stageFile):
		file = open(stageFile)
		data = json.loads(file.read())
		self.start = data["start"]
		self.maps = {}
		self.doors = {}
		for room in data["rooms"]:
			self.maps[room] = Map(filename=data["rooms"][room]["map"])
			self.doors[room] = {}
			for door in data["rooms"][room]["doors"]:
				self.doors[room][door] = data["rooms"][room]["doors"][door]
			
		file.close()

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

