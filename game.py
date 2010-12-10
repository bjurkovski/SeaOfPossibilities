from state import *
from character import *
from stage import *
from item import *
from player import *
from music import *

import sys

from direct.actor.Actor import Actor
from panda3d.core import Point2, Point3
from panda3d.core import LightRampAttrib
from direct.filter.CommonFilters import CommonFilters

class Game(State):
	mapOffset = {"up": (0,1), "down": (0,-1), "left": (-1,0), "right": (1,0)}

	def __init__(self, stage, characters, player, player2):
		State.__init__(self)

		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.player = player
		self.player2 = player2
		self.stage = stage
		self.room = self.stage.start
		self.isOver = False

		self.players = []

		self.startMap()

		self.stage.playMusic()

		# initialize character status string
		self.statusString = OnscreenText(mayChange= True ,
		                                 style=1, fg=(1,1,1,1),
		                                 pos=(0.7,-0.75), scale = .08)


		self.liftables = []

	def spawnObject(self, ob ):

		try:
			if ob.type == "item":
				print('need to make item')
		except AttributeError as e:
			print('Attr error, ', ob , e)

		ob.setMap(self.currentMap())
		ob.getNode().reparentTo(NodePath(self.currentMap().getNode()))
		x,y = self.currentMap().posToGrid(ob.getPos())

		print(ob.name, ob.getPos() )
		print(x,y)

		try:
			self.currentMap().tiles[Map.COLLISION][y][x] = ob.symbol
		except IndexError as e:
			print('Index error: ' , ob.id, e )

	def currentMap(self):
		return self.stage.maps[self.room]

	def exitMap(self):

		for b in self.currentMap().blocks:
			x,y = self.currentMap().posToGrid(b.originalPos)
			print(x,y)
			self.currentMap().tiles[1][y][x] = 'b'

		NodePath(self.currentMap().getNode()).detachNode()

	def startMap(self):
		if not self.currentMap().started:
			for obstacle in self.currentMap().obstacles:
				self.spawnObject(obstacle)

			for item in self.currentMap().items:
				self.spawnObject(item)

			for block in self.currentMap().blocks:
				self.spawnObject(block)

			for liftable in self.currentMap().liftables:
				self.spawnObject(liftable)

			self.currentMap().started = True

			for e in self.currentMap().enemies:
				self.spawnObject(e)

		self.characters[self.player].setMap(self.currentMap())
		self.characters[self.player2].setMap(self.currentMap())

	def changeMap(self,direction):
		self.exitMap()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(self.node)

		map = self.stage.maps[self.room]
		x, y = self.currentMap().posToGrid(self.characters[self.player].getPos())
		if   direction == "right": x = 1
		elif direction == "left":  x = map.width-2
		elif direction == "down":  y = 1
		elif direction == "up":    y = map.height-2
		pos = self.currentMap().gridToPos((x,y))
		self.characters[self.player].setPos(pos)
		self.characters[self.player2].setPos(pos)
		self.characters[self.player2].setDirection(self.characters[self.player].direction)


		self.startMap()

	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())

		char = self.characters[self.player]
		self.players.append(HumanPlayer(char, keys))

		char2 = self.characters[self.player2]
		self.players.append(HumanPlayer(char2 , keys))

		for char in self.characters.values():
			char.getNode().reparentTo(self.node)

		for l in self.stage.getLights():
			render.setLight(l)

		#COWABUNGA comment this to stop the madness
		#render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 1))
		#render.setAttrib(LightRampAttrib.makeDoubleThreshold(0.1, 0.3, 0.9 , 1))
		#render.setAttrib(LightRampAttrib.makeSingleThreshold(0.5, 0.4))

		# THE TRUE CARTOON SHADER :P
#		self.separation = 1 # Pixels
		self.filters = CommonFilters(base.win, self.camera.camera)
		# cell shading
#		filterok = self.filters.setCartoonInk(separation=self.separation)
		# glow
#		filterok = self.filters.setBloom(blend=(0.5,0.5,0.5,1), desat=-0.5, intensity=1.0, size="small")

		self.camera.setPos(0, -2.5, -2.5)
		self.camera.lookAt(0, 0, 0)

	def iterate(self):
		State.iterate(self)
		self.camera.look()

		#self.sendCommands()
		#self.processActions()
		self.move()
		self.buryDeadPeople()

		#let's try
		self.statusString.setText('Room: ' + self.room + '\n' + self.characters[self.player].getStatus())

		if self.isOver:
			return "GameOver"
		elif self.keys['start']:
			return "Paused"

	def move(self):
		for char in [self.characters[self.player], self.characters[self.player2]]:
		#char = self.characters[self.player]
			add = "1"
			if char == self.characters[self.player]:
				add = ""

			directions = [key for key in ["up","down","left","right"] if self.keys[key+add]]

			if self.keys['attack']:
				self.keys['attack'] = False
				print('Using %s' % (char.currentItem()) )

			if self.keys['cancel']:
				self.keys['cancel'] = False
				print('Changing slot')
				char.changeSlot()

			if self.keys['action'] and char.lifting:
				print 'atirando'
				char.lifting.setHeight(0)
				char.lifting.move(char.direction)
				self.liftables.append(char.lifting)
				char.lifting = None

			# I know the block movement code sucks by now... i was just testing it and will refactor

			# BLOCK MOVEMENT ACTION
			for block in self.currentMap().blocks:
				if block.isMoving:
					block.move(block.direction)

			# LIFTABLE MOVEMENT ACTION
			for liftable in self.liftables:
				if liftable.isMoving:
					liftable.move(liftable.direction)

			if len(directions) == 0:
				char.stop()

			p1, p2 = char.getCollisionPos(char.direction)
			x1, y1 = self.currentMap().posToGrid(p1)
			x2, y2 = self.currentMap().posToGrid(p2)
			# BLOCK MOVEMENT TRIGGER
			for x,y in [(x1,y1), (x2,y2)]:
				if self.keys["action"+add] and self.stage.maps[self.room].tileType(1, (x,y)) == 'block':
					for block in self.currentMap().blocks:
						if tuple(self.currentMap().posToGrid(block.getPos())) == (x,y):
							block.move(char.direction)

			for dir in directions:
				#TODO to be re-refactored
				p1, p2 = char.getCollisionPos(dir)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)

				isFree = (self.currentMap().tileType(Map.COLLISION, (x1,y1)) == 'free') and (self.currentMap().tileType(Map.COLLISION, (x2,y2)) == 'free')
				if  isFree:
					char.move(dir)
					if char.lifting:
						char.lifting.setPos(char.getPos())

					ex = self.stage.maps[self.room].getExit((x1,y1))

					if ex and (ex in self.stage.doors[self.room].keys()):
						self.changeMap(ex)
				else:
					char.setDirection(dir)

			p1, p2 = char.getCollisionPos(char.direction)
			x1, y1 = self.currentMap().posToGrid(p1)
			x2, y2 = self.currentMap().posToGrid(p2)
			for x,y in [(x1,y1), (x2,y2)]:
				if self.keys["action"+add] and self.currentMap().tileType(Map.COLLISION, (x,y)) == 'liftable':
					for liftable in self.currentMap().liftables:
						lPos = self.currentMap().posToGrid(liftable.getPos())
						if tuple(lPos) == (x,y):
							char.pick(liftable)
							self.currentMap().tiles[1][y][x] = ' '
							self.keys["action"+add] = False

				if self.stage.maps[self.room].tileType(1, (x,y)) == 'item':
					for item in self.currentMap().items:
						print(item.getPos() ,(x,y))
						if tuple( item.getPos() ) == (x,y):
							print("colidindo mesmo")
							self.collision(char, item)

				elif self.stage.maps[self.room].tileType(1, (x,y)) == 'enemy':
					for enemy in self.currentMap().enemies:
						if tuple(enemy["pos"]) == (x,y):
							self.collision(char, enemy["instance"])

	def collision(self, a, b):
		print "TYPE A:", a.getType(), "TYPE B:", b.getType()

		# commented while fixing the bugs
		if b.getType() == 'item':
			for i in range(len(self.currentMap().items)):
				if tuple(self.currentMap().items[i]["instance"].getPos()) == tuple(b.getPos()):
					self.currentMap().items.pop(i)
					x, y = self.currentMap().posToGrid((NodePath(b.getNode()).getX(), NodePath(b.getNode()).getZ()))
					self.currentMap().tiles[1][y][x] = ' '
					NodePath(b.getNode()).removeNode()

					# again this is idiotic, but forgive me
					a.pickItem(b.extra)

		if a.getType() == 'Character':
			print("Collided with", b.getType())
			if b.getType() == 'enemy':
				if len(self.currentMap().items) == 0:
					b.takeDamage(1)
				else:
					a.takeDamage(1)

	def buryDeadPeople(self):
		# commented while fixing the bugs
		# for enemy in self.currentMap().enemies:
			# if not enemy["instance"].isAlive():
				# x, y = self.currentMap().posToGrid(NodePath(enemy["instance"].getNode()).getPos())
				# self.currentMap().tiles[1][y][x] = ' '
				# NodePath(enemy["instance"].getNode()).removeNode()
				# self.currentMap().enemies.remove(enemy)
				# #self.currentMap().enemies.pop(e)

		#if not self.player.isAlive() : #tratar isso corretamente!
		for char in self.characters:
			if not self.characters[char].isAlive():
				self.isOver = True


# to do (or not): create GameServer and GameClient classes to inherit from Game

