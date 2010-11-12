
import json

from item import Item
from model import Model
from character import Character

from panda3d.core import NodePath, CardMaker, Texture, Vec4, Point3
from panda3d.core import PointLight, DirectionalLight, AmbientLight, Spotlight
from direct.actor.Actor import Actor

tex = Texture('tex')
#tex.load('tex/grass.png')
#tex.load('tex/grass_painterly.jpg')
#tex.load('tex/grasspaint.png')
tex.load('tex/grass_painterly_large.jpg')

class Map:
	def __init__(self, filename=None, size=()):
		self.started = False
		self.tiles = []
		self.cards = []
		self.items = []
		
		self.nodePath = None
		
		self.itens_ref = Item('cfg/itens.json')

		self.readConfig()

		if filename != None:
			try:
				file = open(filename)
				data = json.loads(file.read())
				file.close()

				self.tiles = data["map"]

				for layer in range(len(self.tiles)):
					for y in range(len(self.tiles[layer])):
						self.tiles[layer][y] = list(self.tiles[layer][y])

				#reading map metadata
				try: 
					for i in data["items"]:
						instance = self.itens_ref.getInstance( i['name'] )
						instance['pos'] = i['pos']
						self.items.append(instance) 
				except KeyError: self.items = []
					
				try: self.enemies = data["enemies"]
				except KeyError: self.enemies = []

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

	def readConfig(self):

		cfg = open("cfg/stage.cfg")
		
		data = json.loads(cfg.read())
		self.tilemap = data['tilemap']
		
		cfg.close()

	def tileIs(self, layer, point, tilename):
		return tilename == self.tilemap[self.tiles[layer][int(point[1])][int(point[0])]]

	def posIs(self, layer, pos, tilename):
		x,y = self.posToGrid(pos)
		return self.tileIs(layer, (x,y), tilename)

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
		#the ground
		cm = CardMaker('CardMaker')
		cm.setFrame(-2,2,-2,2)
		card = self.nodePath.attachNewNode(cm.generate())
		card.setTexture(tex)

		for y in range(self.height):
			for x in range(self.width):
				#THIS could use a refactor
				if self.tileIs(1, (x,y), 'obstacle'):
					self.obstacles.append( self.makeObject('obstacle',x,y) )

				elif self.tileIs(1, (x,y), 'block' ):
					self.blocks.append(self.makeObject('block',x,y))

				elif self.tileIs(1, (x,y), 'tree' ):
					self.blocks.append(self.makeObject('tree',x,y))

	def makeObject(self, obj_type, x, y):
		# THIS SHOULD NOT BE NECESSARY. TO DO: THEME FILE WITH THIS DICTs
		# yeah I know
		models = { 'block' : 'block', 'obstacle' : 'rock', 'tree' : 'tree' }
		symbols = { 'block' : 'b', 'obstacle' : "o", 'tree' : 't' }
		types = { 'obstacle' : 'obstacle', 'tree' : 'obstacle', 'block' : 'block'}
		obj = {"pos" : (x,y), 
				"instance" : Model("model/" + models[obj_type] + ".json") , 
				"name" : types[obj_type],
				"symbol" :  symbols[obj_type] ,
				"type" : obj_type 
			  }

		return obj
		
	def posToGrid(self, pos):
		#x = int(round(self.width/2 + (pos[0]-self.squareWidth/2)/self.squareWidth))
		x = int(round(self.width/2 + (pos[0])/self.squareWidth))

		##y = self.height-1 - int(round(self.height/2 + (pos[1]-self.squareHeight/2)/self.squareHeight))
		#y = self.height-1 - int(round(self.height/2 + (pos[1]-self.squareHeight/2)/self.squareHeight))
		y = self.height-1 - int(round(self.height/2 + (pos[1])/self.squareHeight))
		
		return (x,y)
	
	def gridToPos(self, grid):
		#x = (grid[0] - self.width/2)*self.squareWidth + self.squareWidth/2
		x = (grid[0] - self.width/2)*self.squareWidth
		
		##y = -(grid[1] + self.squareHeight/2 - self.height/2 + 1) * self.squareHeight
		#y = - (grid[1] - self.height + 1 + self.height/2)*self.squareHeight + self.squareHeight/2
		y = -(grid[1] - self.height + 1 + self.height/2)*self.squareHeight
		
		return (x,y)

	def getNode(self):
		return self.nodePath.node()

class Stage:

	def __init__(self, stageFile):
		file = open(stageFile)
		data = json.loads(file.read())

		self.readLights(data['lights'])

		self.start = data["start"]
		self.maps = {}
		self.doors = {}
		for room in data["rooms"]:
			self.maps[room] = Map(filename=data["rooms"][room]["map"])
			self.doors[room] = {}
			for door in data["rooms"][room]["doors"]:
				self.doors[room][door] = data["rooms"][room]["doors"][door]
			
		file.close()

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
				self.lights.append( NodePath(pl) )

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

