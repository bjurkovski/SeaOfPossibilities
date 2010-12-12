import json

from item import Item
from model import Model
from character import Character
from music import Music
from switch import Switch
from panda3d.core import NodePath, CardMaker, Texture, Vec4, Point3
from panda3d.core import PointLight, DirectionalLight, AmbientLight, Spotlight
from direct.actor.Actor import Actor

tex = Texture('tex')
tex.load('tex/grass_painterly_large.jpg')

class Map:
	GROUND = 0
	COLLISION = 1
	def __init__(self, data):
		self.started = False
		self.tiles = []
		self.items = []

		self.nodePath = None

		self.readConfig()

		try:
			self.tiles = data["map"]

			for layer in range(len(self.tiles)):
				for y in range(len(self.tiles[layer])):
					self.tiles[layer][y] = list(self.tiles[layer][y])

		except IOError as e:
			print e
			print "Error creating map: %s not found." % filename
			exit()

		self.height, self.width = len(self.tiles[Map.GROUND]), len(self.tiles[Map.GROUND][0])
		self.squareHeight, self.squareWidth = 2.0/self.height, 2.0/self.width

		#reading map metadata
		try:
			items = data["items"]
		except KeyError as e:
			self.items = []

		try:
			for i in items:
				item = Item(i['name'])
				item.setPos(self.gridToPos( i['pos'] ) )
				item.originalPos = item.getPos()
				self.items.append(item)
		except KeyError as e:
			# ESSA PORRA NAO TINHA QUE TAR AQUI!!! TEMOS QUE PARAR DE PEGAR EXCECOES INUTEIS.....
			# Nao meu, o mapa pode vir se o campo itens e o programa nao pode fechar...
			print('Error reading items: %s' % e)
			self.items = []

		try:
			self.enemies = data["enemies"]
			self.enemies = [ self.makeCharacter(e,'enemy') for e in self.enemies ]
			print(self.enemies)
		except KeyError as e:
			self.enemies = []

		self.constructModel()

	def readConfig(self):
		cfg = open("cfg/stage.cfg")
		data = json.loads(cfg.read())
		self.tilemap = data['tilemap']
		cfg.close()

	def tileType(self, layer, point):
		return self.tilemap[self.tiles[layer][int(point[1])][int(point[0])]]

	def futPosAreFree(self, p1, p2):
		x1, y1 = self.posToGrid(p1)
		x2, y2 = self.posToGrid(p2)

		return (self.tileType(Map.COLLISION, (x1,y1)) == 'free') and (self.tileType(Map.COLLISION, (x2,y2)) == 'free')

	def getExit(self,point):
		"""
			Returns a string representing the direction if the given point
			is an exit and None if it's not.
		"""
		direc = None

		minX, maxX = 0, self.width-1
		minY, maxY = 0, self.height-1

		# in the first line
		if point[1] == maxY:
			return "down"
		# in the last line
		if point[1] == 0:
			return "up"
		if point[0] == 0:
			return "left"
		if point[0] == maxX:
			return "right"

		return direc

	def __str__(self):
		# WRONG!!!!
		str = ""
		for row in self.tiles[Map.COLLISION]:
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
		self.liftables = []
		self.switches = []

		if self.nodePath != None:
			self.nodePath.removeNode()
			self.cards = []

		self.nodePath = NodePath("Map")
		#the ground
		cm = CardMaker('CardMaker')
		cm.setFrame(-2,2,-2,2)
		card = self.nodePath.attachNewNode(cm.generate())
		card.setTexture(tex)

		for y in range(self.height):
			for x in range(self.width):
				tType = self.tileType(Map.GROUND, (x,y))

				if tType == 'inactive_switch':
					self.switches.append(self.makeSwitch(x, y))

		for y in range(self.height):
			for x in range(self.width):
				# TO DO: MUDAR NOME
				a = {"block": self.blocks,
					 "obstacle": self.obstacles,
					 "tree": self.obstacles,
					 "liftable": self.liftables}
				tType = self.tileType(Map.COLLISION, (x,y))

				if tType != 'free':
					a[tType].append(self.makeObject(tType, x,y))

	def makeSwitch(self, x, y):
		switch = Switch(self.squareHeight, self.squareWidth)
#		switch.model.setColor(0, 0, 0)
		x,y = self.gridToPos((x,y))
		switch.setPos(x,y)
		return switch
		#cm = CardMaker('CardMaker-Switches')
		#cm.setFrame(-0.2, .2, -0.2, 0.2)
		#card = self.nodePath.attachNewNode(cm.generate())
		#card.setTexture(tex)

	def makeObject(self, obj_type, x, y):
		# THIS SHOULD NOT BE NECESSARY. TO DO: THEME FILE WITH THIS DICTs
		# yeah I know
		models = { 'block': 'block', 'obstacle': 'rock', 'tree': 'tree', "liftable": "liftable" }
		symbols = { 'block': 'b', 'obstacle': "o", 'tree': 't', 'liftable': 'l' }
		types = { 'obstacle': 'obstacle', 'tree': 'obstacle', 'block': 'block', 'liftable': 'liftable'}

		instance = Model("model/" + models[obj_type] + ".json")
		instance.setPos(self.gridToPos((x,y)))
		instance.originalPos = instance.getPos()
		instance.name = types[obj_type]
		instance.symbol = symbols[obj_type]
		instance.type = obj_type

		return instance

	def makeCharacter(self,char,cType):
		c = Character('char/' + char['name'])
		c.setPos(self.gridToPos(char['pos']))
		c.originalPos = self.gridToPos(char['pos'])
		c.type = cType
		# GAMBIT
		c.symbol = cType[0]
		c.name = char['name']

		return c

	def posToGrid(self, pos):
		x = int(round(self.width/2 + (pos[0])/self.squareWidth))
		y = self.height-1 - int(round(self.height/2 + (pos[1])/self.squareHeight))

		return (x,y)

	def gridToPos(self, grid):
		x = (grid[0] - self.width/2)*self.squareWidth
		y = -(grid[1] - self.height + 1 + self.height/2)*self.squareHeight

		return (x,y)

	def getNode(self):
		return self.nodePath.node()

class Stage:

	def __init__(self, stageFile, mapFile = None):
		stFile = open(stageFile)

		if mapFile:
			mpFile = open(mapFile)

		data = json.loads(stFile.read())

		if mapFile:
			mapData = json.loads(mpFile.read())

		self.readLights(data["lights"])

		self.start = data["start"]

		self.maps = {}
		self.doors = {}

		#could be better
		self.music = Music(data['name'])
		self.music.addTrack(data['music'])
		self.music.setCurrent(data['music'])

		for room in data["rooms"]:

			self.maps[room] = Map(mapData[room])

			self.doors[room] = {}

			for door in data["rooms"][room]:
				self.doors[room][door] = data["rooms"][room][door]

		stFile.close()
		mpFile.close()

	def setTrack(self,title):
		self.music.setTrack(title)

	def playMusic(self):
		self.music.play()


	def readLights(self,light_data):
		self.lights = []
		i = 0

		for light in light_data:
			name = '%s light %d' % (light['type'], i )
			pl = None

			if light['type'] == 'point':
				pl = PointLight( name )
				pl.setPoint(Point3(*light['pos']))
				pl.setColor(Vec4(*light['color']) )

			elif light['type'] == 'directional':
				pl = DirectionalLight( name )
				pl.setColor(Vec4(*light['color']) )

			elif light['type'] == 'ambient':
				pl = AmbientLight( name )
				pl.setColor(Vec4(*light['color']) )

			#not implemented
			#elif light['type'] == 'spotlight':
			#	pl = Spotlight( name )

			#if it's allright
			if pl != None:
				self.lights.append(NodePath(pl))

			i += 1

	def getLights(self):
		return self.lights

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

