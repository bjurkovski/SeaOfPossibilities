import json
from panda3d.core import NodePath, CardMaker, Texture
from direct.actor.Actor import Actor

tex = Texture('tex') #loader.loadTexture('tex/grass.png')
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

	def readConfig(self):

		cfg = open("cfg/stage.cfg")	
		
		data = json.loads(cfg.read())
		self.tilemap = data['tilemap']
		
		cfg.close()

	# sets all the points considered to be exits 
	def setExits(self,direction,where):
		self.exits = { 'up' : [], 'down' : [], 'right' : [], 'left' : [] }

		if direction == 'up':
			for i in range(tiles[0].size):
				x , y = 0,i
				if self.isTile(tiles[x][y], 'clear'):
					self.exits['up'].append( (x,y) )

		elif direction == 'down':
			for i in range(tiles[0].size):
				x , y = tiles.size,i
				if self.isTile(tiles[x][y], 'clear'):
					self.exits['down'].append( (x,y) )

		elif direction == 'right':
			for i in range(tiles.size):
				x , y = i,tiles.size
				if self.isTile(tiles[x][y], 'clear'):
					self.exits['right'].append( (x,y) )

		elif directon == 'left':
			for i in range(tiles[0].size):
				x , y = i,0
				if self.isTile(tiles[x][y], 'clear'):
					self.exits['left'].append( (x,y) )
				

	def getExit(self,point):
		"""
			Returns a string representing the direction if the given point
			is an exit and None if it's not. 
		"""
		pass

	def tileIs(self, tile , tilename):
		return tile == self.tilemap[tilename]

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
				card.setPos(sx/2 + i*sx - 1 , 0, sy/2 + j*sy - 1)
				
				card.setTexture(tex)
				
				self.cards[i].append(card)
				card.reparentTo(self.nodePath)
				
				if self.tilemap[self.tiles[i][j]] == 'obstacle':
					m = Actor('model/rock/rock') 
					m.reparentTo(card)
					m.setHpr(0,90,0)
					m.setScale(0.015,0.015,0.015)

	def getNode(self):
		return self.nodePath.node()

class Stage:
	def __init__(self, stageFile):
		file = open(stageFile)
		data = json.loads(file.read())
		self.start = data["start"]
		self.maps = {}
		for room in data["rooms"]:
			self.maps[room] = Map(filename=data["rooms"][room]["map"])
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

