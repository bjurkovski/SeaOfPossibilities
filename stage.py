import json
from panda3d.core import NodePath, CardMaker, Texture
from direct.actor.Actor import Actor
from model import Model
from character import Character

tex = Texture('tex')
tex.load('tex/grass.png')

class Map:
	def __init__(self, filename=None, size=()):
		self.started = False
		self.tiles = []
		self.cards = []
		self.nodePath = None

		self.readConfig()

		if filename != None:
			try:
				file = open(filename)
				data = json.loads(file.read())
				file.close()
				self.tiles = data["map"]
				
				# the tiles are read as string, so we need to convert them
				# to a list to manipulate them
				for layer in range(len(self.tiles)):
					for y in range(len(self.tiles[layer])):
						self.tiles[layer][y] = list(self.tiles[layer][y])

				try:
					self.items = data["items"]
				except KeyError:
					self.items = []
					
				try:
					self.enemies = data["enemies"]
				except KeyError:
					self.enemies = []
				#self.tiles = data["map"].split()
			except IOError:
				print "Error creating map: %s not found." % filename
				exit()
		elif size != ():
			try:
				self.tiles.append([])
				for layer in range(size[2]):
					for i in range(size[0]):
						self.tiles[layer].append([])
						for j in range(size[1]):
							self.tiles[layer][i].append(' ')
			except:
				print "Error creating map: expecting a size=(width, height)."
				exit()
		else:
			print "Error creating map: please provide either the filename or the size to be allocated."
			exit()

		self.height, self.width = len(self.tiles[0]), len(self.tiles[0][0])
		self.squareHeight, self.squareWidth = 2.0/self.height, 2.0/self.width

		self.constructModel()

		print(self)

	def readConfig(self):

		cfg = open("cfg/stage.cfg")	
		
		data = json.loads(cfg.read())
		self.tilemap = data['tilemap']
		
		cfg.close()

	def tileIs(self, layer, point, tilename):
		#print layer, point[1], point[0]
		return tilename == self.tilemap[self.tiles[layer][int(point[1])][int(point[0])]]


	def getExit(self,point):
		"""
			Returns a string representing the direction if the given point
			is an exit and None if it's not. 
		"""
		direc = None
		clear = self.tileIs(0, point, 'ground')
		
		minX, maxX = 0, self.width-1
		minY, maxY = 0, self.height-1
		
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
		for row in self.tiles[0]:
			for tile in row:
				str += tile
			str += "\n"
		return str

	def save(self, filename):
		file = open(filename, 'w')
		file.write(self.__str__())
		file.close()

	def constructModel(self):
		self.obstacles = []
		self.blocks = []

		if self.nodePath != None:
			self.nodePath.removeNode()
			self.cards = []

		self.nodePath = NodePath("Map")
		cm = CardMaker('CardMaker')

		for y in range(self.height):
			self.cards.append([])
			for x in range(self.width):
				cm.setFrame(self.squareWidth/2, -self.squareWidth/2, self.squareHeight/2, -self.squareHeight/2)
				card = self.nodePath.attachNewNode(cm.generate())
				card.setPos((self.squareWidth/2 + x*self.squareWidth - 1), 0, -(self.squareHeight/2 + y*self.squareHeight - 1))
				
				card.setTexture(tex)
				
				self.cards[y].append(card)
				card.reparentTo(self.nodePath)
				
				#THIS could use a refactor
				if self.tileIs(1, (x,y), 'obstacle'):
					self.obstacles.append( self.makeObject('obstacle',x,y) )

				if self.tileIs(1, (x,y), 'block' ):
					self.blocks.append(self.makeObject('block',x,y))

	def makeObject(self, obj_type, x, y):
		models = { 'block' : 'block', 'obstacle' : 'rock' }

		obj = {"pos" : (x,y), 
				"model" : "model/" + models[obj_type] + ".json", 
				"name" : obj_type }

		return obj

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

