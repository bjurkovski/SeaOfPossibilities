from state import *
from character import *
from stage import *
from item import *
from player import *
from music import *
import random

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

		self.players = [player,player2]
		#print(self.players)
		self.startMap()

		self.stage.playMusic()
		self.status = []

		posi = 0
		for p in self.players:
			# initialize character status string
			self.status.append (OnscreenText(mayChange= True ,
				                             style=1, fg=(1,1,1,1),
				                             pos=(1.5*posi - 0.7,-0.75), scale = .08)
			)
			posi += 1

	def spawnObject(self, ob ):
		try:
			if ob.type == "item":
				print('need to make item')
		except AttributeError as e:
			print('Attr error, ', ob , e)

		ob.setMap(self.currentMap())
		ob.getNode().reparentTo(NodePath(self.currentMap().getNode()))
		x,y = self.currentMap().posToGrid(ob.getPos())


		try:
			self.currentMap().tiles[Map.COLLISION][y][x] = ob.symbol
		except IndexError as e:
			print('Index error: ' , ob.id, e )

	def currentMap(self):
		return self.stage.maps[self.room]

	def exitMap(self):
		for i in range(self.currentMap().width):
			for j in range(self.currentMap().height):
				atype = self.currentMap().tileType(1,(i,j))
				if atype == 'block' or atype == 'liftable':
					self.currentMap().tiles[1][j][i] = ' '

		for b in self.currentMap().blocks:
			b.setPos(b.originalPos)
			x,y = self.currentMap().posToGrid(b.getPos())
			self.currentMap().tiles[1][y][x] = 'b'

		for b in self.currentMap().liftables:
			b.setPos(b.originalPos)
			x,y = self.currentMap().posToGrid(b.getPos())
			self.currentMap().tiles[1][y][x] = 'l'
			b.getNode().reparentTo(NodePath(self.currentMap().getNode()))

		for char in [self.characters[self.player], self.characters[self.player2]]:
			char.lifting = None

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

			for switch in self.currentMap().switches:
				switch.getNode().reparentTo(NodePath(self.currentMap().getNode()))

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
		render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 1))
		#render.setAttrib(LightRampAttrib.makeDoubleThreshold(0.1, 0.3, 0.9 , 1))
		#render.setAttrib(LightRampAttrib.makeSingleThreshold(0.5, 0.4))

		# THE TRUE CARTOON SHADER :P
#		self.separation = 1 # Pixels
		self.filters = CommonFilters(base.win, self.camera.camera)
		# cell shading
#		filterok = self.filters.setCartoonInk(separation=self.separation)
		# glow
		filterok = self.filters.setBloom(blend=(0.5,0.5,0.5,1), desat=-0.5, intensity=0.5, size="small")

		self.camera.setPos(0, -2.5, -2.5)
		self.camera.lookAt(0, 0, 0)

	def iterate(self):
		State.iterate(self)
		self.camera.look()

		for e in self.currentMap().enemies:
			e.IsMoving = True

		self.moveObjects()
		self.doCharActions()
		self.moveChars()
		self.buryDeadPeople()

		#let's try
		for i in range(2):
			self.status[i].setText(self.characters[self.players[i]].getStatus())

		if self.isOver:
			return "GameOver"
		elif self.keys['start']:
			return "Paused"

	def moveObjects(self):
		# BLOCK MOVEMENT ACTION
		for block in self.currentMap().blocks:
			if block.isMoving:
				block.move(block.direction)

		# LIFTABLE MOVEMENT ACTION
		for liftable in self.currentMap().liftables:
			if liftable.isMoving:
				liftable.move(liftable.direction)
				p1, p2 = liftable.getCollisionPos(liftable.direction)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)
				for x,y in [(x1,y1), (x2,y2)]:
					if self.stage.maps[self.room].tileType(1, (x,y)) == 'enemy':
						for enemy in self.currentMap().enemies:
							lPos = self.currentMap().posToGrid(enemy.getPos())
							if tuple(lPos) == (x,y):
								self.collision(liftable, enemy)

	def doCharActions(self):
		for char in [self.characters[self.player], self.characters[self.player2]]:
			add = "1"
			if char == self.characters[self.player]:
				add = ""

			if self.keys['attack'+add]:
				self.keys['attack'] = False
				print('Using %s' % (char.currentItem()) )

			if self.keys['cancel'+add]:
				self.keys['cancel'] = False
				print('Changing slot')
				char.changeSlot()

			if self.keys['action'+add] and char.lifting:
				print 'atirando'
				char.lifting.setHeight(0)
				char.lifting.move(char.direction)
				char.lifting = None

	def moveChars(self):
		for char in [self.characters[self.player], self.characters[self.player2]]:
			add = "1"
			if char == self.characters[self.player]:
				add = ""

			directions = [key for key in ["up","down","left","right"] if self.keys[key+add]]

			# I know the block movement code sucks by now (REALLY?)... i was just testing it and will refactor

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

			for enemy in self.currentMap().enemies:
				#TODO actually enemies are still present in the map
				x,y = self.currentMap().posToGrid(enemy.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = ' '
				dir = ['up','down','left','right'][random.randint(0,3)]
				p1, p2 = enemy.getCollisionPos(dir)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)

				isFree = (self.currentMap().tileType(Map.COLLISION, (x1,y1)) == 'free') and (self.currentMap().tileType(Map.COLLISION, (x2,y2)) == 'free')
				if  isFree:
					enemy.move(dir)
				else:
					enemy.setDirection(dir)

				x,y = self.currentMap().posToGrid(enemy.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = 'e'

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

				collisionTiles = ["item", "enemy"]
				collisionElements = {"item": self.currentMap().items, "enemy": self.currentMap().enemies}

				for t in collisionTiles:
					if self.stage.maps[self.room].tileType(1, (x,y)) == t:
						for e in collisionElements[t]:
							lPos = self.currentMap().posToGrid(e.getPos())
							if tuple(lPos) == (x,y):
								self.collision(char, e)

				# the part down here was generalized in the code above
				#if self.stage.maps[self.room].tileType(1, (x,y)) == 'item':
				#	for item in self.currentMap().items:
				#		lPos = self.currentMap().posToGrid(item.getPos())
				#		if tuple(lPos) == (x,y):
				#			self.collision(char, item)
				#
				#elif self.stage.maps[self.room].tileType(1, (x,y)) == 'enemy':
				#	for enemy in self.currentMap().enemies:
				#		lPos = self.currentMap().posToGrid(enemy.getPos())
				#		if tuple(lPos) == (x,y):
				#			self.collision(char, enemy)

	def collision(self, a, b):
		print "Collision: TYPE A:", a.getType(), "TYPE B:", b.getType()

		# commented while fixing the bugs
		if b.getType() == 'item':
			for i in range(len(self.currentMap().items)):
				if tuple(self.currentMap().items[i].getPos()) == tuple(b.getPos()):
					self.currentMap().items.pop(i)
					x, y = self.currentMap().posToGrid((NodePath(b.getNode()).getX(), NodePath(b.getNode()).getZ()))
					self.currentMap().tiles[1][y][x] = ' '
					NodePath(b.getNode()).removeNode()

					# again this is idiotic, but forgive me
					print "need to pick the item somehow..."
					a.pickItem(b)

		if a.getType() == 'liftable' and b.getType() == 'enemy':
			a.stop()
			a.getNode().detachNode()
			x,y = self.currentMap().posToGrid(a.getPos())
			self.currentMap().tiles[Map.COLLISION][y][x] = ' '
			b.takeDamage(10000)


		if a.getType() == 'Character':
			print("Character collided with", b.getType())
			if b.getType() == 'enemy':
				a.takeDamage(1)

	def buryDeadPeople(self):
		# commented while fixing the bugs
		for enemy in self.currentMap().enemies:
			if not enemy.isAlive():
				x, y = self.currentMap().posToGrid(NodePath(enemy.getNode()).getPos())
				self.currentMap().tiles[1][y][x] = ' '
				NodePath(enemy.getNode()).removeNode()
				self.currentMap().enemies.remove(enemy)

		#if not self.player.isAlive() : #tratar isso corretamente!
		for char in self.characters:
			if not self.characters[char].isAlive():
				self.isOver = True


# to do (or not): create GameServer and GameClient classes to inherit from Game

