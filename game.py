from state import *
from character import *
from stage import *
from item import *
from player import *
from music import *
from sprite import *

import random
import sys

from direct.actor.Actor import Actor
from panda3d.core import Point2, Point3
from panda3d.core import LightRampAttrib
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText

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

		#print(self.players)
		self.startMap()

		self.stage.playMusic()
		self.status = {}

		posi = 0
		for c in self.characters:
			# initialize character status string
			self.status[c] = (OnscreenText(mayChange= True ,
				                             style=2, fg=(1,1,1,1),
				                             pos=(1.5*posi - 0.7,-0.85), scale = .08)
			)
			posi += 1

	def spawnObject(self, ob):
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
			self.currentMap().tiles[Map.COLLISION][y][x] = 'b'
			b.getNode().reparentTo(NodePath(self.currentMap().getNode()))

		for b in self.currentMap().liftables:
			b.setPos(b.originalPos)
			x,y = self.currentMap().posToGrid(b.getPos())
			self.currentMap().tiles[Map.COLLISION][y][x] = 'l'
			b.getNode().reparentTo(NodePath(self.currentMap().getNode()))

		for d in self.currentMap().doors:
			if d.permanent:
				x,y = self.currentMap().posToGrid(d.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = 'd'
				d.getNode().reparentTo(NodePath(self.currentMap().getNode()))

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

			for door in self.currentMap().doors:
				self.spawnObject(door)

			self.currentMap().started = True

			for e in self.currentMap().enemies:
				self.spawnObject(e)

		self.characters[self.player].setMap(self.currentMap())
		self.characters[self.player2].setMap(self.currentMap())

	def changeMap(self,direction,char):
		#TODO modularize for more characters
		self.exitMap()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(self.node)

		map = self.stage.maps[self.room]
		x, y = self.currentMap().posToGrid(char.getPos())
		if   direction == "right": x = 1
		elif direction == "left":  x = map.width-2
		elif direction == "down":  y = 1
		elif direction == "up":    y = map.height-2
		pos = self.currentMap().gridToPos((x,y))

		self.characters[self.player].setPos(pos)
		self.characters[self.player2].setPos(pos)
		self.characters[self.player2].setDirection(self.characters[self.player].direction)


		self.startMap()

	def register(self, render, camera, keys, render2d):
		State.register(self, render, camera, keys, render2d)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())


		for c in self.characters:
			self.status[c].reparentTo(self.node2d)

		for char in self.characters.values():
			char.getNode().reparentTo(self.node)

		for l in self.stage.getLights():
			render.setLight(l)

		# COWABUNGA test!!!
		self.hearts = {}
		numChar=0

		self.heartsNode = NodePath(PandaNode('hearts'))
		self.heartsNode.reparentTo(self.node2d)

		for char in self.characters:
			self.hearts[char] = []

			for i in range(Character.maxHearts):
				self.hearts[char].append(Sprite("heart.png", 0.05, 0.05))
				self.hearts[char][i].setPos(-0.5 + 1*numChar + (i%3)*0.055 , -0.7 - int(i/3)*0.055)
				self.hearts[char][i].getNode().reparentTo(self.heartsNode)

			numChar += 1

		#COWABUNGA comment this to stop the madness
		render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 1))

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

		self.moveObjects()
		self.doCharActions()
		self.moveChars()
		self.buryDeadPeople()

		self.activateSwitches()

		self.updateHUD()

		if self.isOver:
			return "GameOver"
		elif self.keys['start']:
			return "Paused"

	def updateHUD(self):

		for c in self.characters:
			self.status[c].setText(self.characters[c].getStatus())

			if self.characters[c].healthChanged:
				for heart in self.hearts[c]:
					heart.getNode().detachNode()

				for i in range(self.characters[c].hearts):
					self.hearts[c][i].getNode().reparentTo(self.heartsNode)

				self.characters[c].healthChanged = False

	def moveObjects(self):
		# BLOCK MOVEMENT ACTION
		for block in self.currentMap().blocks:
			if block.isMoving:
				block.move(block.direction)
				p1, p2 = block.getCollisionPos(block.direction)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)
				try:
					for x,y in [(x1,y1), (x2,y2)]:
						if self.stage.maps[self.room].tileType(1, (x,y)) == 'enemy':
							for enemy in self.currentMap().enemies:
								lPos = self.currentMap().posToGrid(enemy.getPos())
								if tuple(lPos) == (x,y):
									self.collision(block, enemy)
						else:
							for char in self.characters:
								if (x,y) == self.currentMap().posToGrid(self.characters[char].getPos()):
									bx,by = self.currentMap().posToGrid(block.getPos())
									self.currentMap().tiles[Map.COLLISION][by][bx] = ' '
									self.characters[char].stun()
									block.stop()
									block.getNode().detachNode()
				except IndexError:
					block.stop()

		# LIFTABLE MOVEMENT ACTION
		for liftable in self.currentMap().liftables:
			if liftable.isMoving:
				liftable.move(liftable.direction)
				p1, p2 = liftable.getCollisionPos(liftable.direction)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)
				try:
					for x,y in [(x1,y1), (x2,y2)]:
						if self.stage.maps[self.room].tileType(1, (x,y)) == 'enemy':
							for enemy in self.currentMap().enemies:
								lPos = self.currentMap().posToGrid(enemy.getPos())
								if tuple(lPos) == (x,y):
									self.collision(liftable, enemy)
						elif self.stage.maps[self.room].tileType(1, (x,y)) != 'free':
							liftable.stop()
							liftable.getNode().detachNode()
						else:
							for char in self.characters:
								if (x,y) == self.currentMap().posToGrid(self.characters[char].getPos()):
									print "Stun nele!"
									self.characters[char].stun()
									liftable.stop()
									liftable.getNode().detachNode()
				except IndexError:
					# to do, create a liftable.destroy(), which animates the liftable and do these two actions:
					liftable.stop()
					liftable.getNode().detachNode()

	def doCharActions(self):
		for char in [self.characters[self.player], self.characters[self.player2]]:
			add = "1"
			if char == self.characters[self.player]:
				add = ""

			if self.keys['attack'+add]:
				self.keys['attack'+add] = False
				print('Using %s' % (char.currentItem()) )
				p1, p2 = char.getCollisionPos(char.direction)
				x1, y1 = self.currentMap().posToGrid(p1)
				x2, y2 = self.currentMap().posToGrid(p2)

				for x,y in [(x1,y1), (x2,y2)]:
					if self.stage.maps[self.room].tileType(Map.COLLISION, (x,y)) == 'door':
						for d in self.currentMap().doors:
							if tuple(self.currentMap().posToGrid(d.getPos())) == (x,y):
								opened = d.open(char.currentItem())
								if opened:
									self.currentMap().tiles[Map.COLLISION][y][x] = ' '
									char.destroyCurrentItem()

			if self.keys['cancel'+add]:
				self.keys['cancel'+add] = False
				print('Changing slot')
				char.changeSlot()

			if self.keys['action'+add]:
				self.keys['action'+add] = False
				if char.lifting:
					char.lifting.setHeight(0)
					char.lifting.move(char.direction)
					char.lifting = None
				else:
					p1, p2 = char.getCollisionPos(char.direction)
					x1, y1 = self.currentMap().posToGrid(p1)
					x2, y2 = self.currentMap().posToGrid(p2)

					for x,y in [(x1,y1), (x2,y2)]:
						if self.stage.maps[self.room].tileType(Map.COLLISION, (x,y)) == 'block':
							for block in self.currentMap().blocks:
								if tuple(self.currentMap().posToGrid(block.getPos())) == (x,y):
									block.move(char.direction)
						elif self.stage.maps[self.room].tileType(Map.COLLISION, (x,y)) == 'item':
							for item in self.currentMap().items:
								if tuple(self.currentMap().posToGrid(item.getPos())) == (x,y):
									self.collision(char, item)
						elif self.currentMap().tileType(Map.COLLISION, (x,y)) == 'liftable':
							for liftable in self.currentMap().liftables:
								lPos = self.currentMap().posToGrid(liftable.getPos())
								if tuple(lPos) == (x,y):
									char.pick(liftable)
									self.currentMap().tiles[1][y][x] = ' '

	def moveChars(self):
		for char in [self.characters[self.player], self.characters[self.player2]]:
			add = "1"
			if char == self.characters[self.player]:
				add = ""

			directions = [key for key in ["up","down","left","right"] if self.keys[key+add]]

			if len(directions) == 0:
				char.stop()

			for dir in directions:
				#TODO to be re-refactored
				p1, p2 = char.getCollisionPos(dir)

				if self.currentMap().futPosAreFree(p1, p2):
					char.move(dir)
					if char.lifting:
						char.lifting.setPos(char.getPos())

					ex = self.stage.maps[self.room].getExit(self.currentMap().posToGrid(p1))

					if ex and (ex in self.stage.doors[self.room].keys()):
						self.changeMap(ex,char)
				else:
					char.setDirection(dir)

			for enemy in self.currentMap().enemies:
				#TODO actually enemies are still present in the map
				x,y = self.currentMap().posToGrid(enemy.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = ' '

				# COWABUNGA
				# se botarmos aqui uma funcao que define como o inimigo anda
				# vai dar tudo certo
				# por exemplo ele pode as vezes andar em direcao a um heroi e
				# as vezes ser random
				# por enquanto e so random
				# - OK, agreed
				dir = ['up','down','left','right'][random.randint(0,3)]
				p1, p2 = enemy.getCollisionPos(dir)

				if self.currentMap().futPosAreFree(p1, p2):
					enemy.enemy_move(dir)
				else:
					enemy.setDirection(dir)

				x,y = self.currentMap().posToGrid(enemy.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = 'e'

			p1, p2 = char.getCollisionPos(char.direction)
			x1, y1 = self.currentMap().posToGrid(p1)
			x2, y2 = self.currentMap().posToGrid(p2)
			for x,y in [(x1,y1), (x2,y2)]:
				collisionTiles = ["enemy"]
				collisionElements = {"enemy": self.currentMap().enemies}

				for t in collisionTiles:
					if self.stage.maps[self.room].tileType(Map.COLLISION, (x,y)) == t:
						for e in collisionElements[t]:
							lPos = self.currentMap().posToGrid(e.getPos())
							if tuple(lPos) == (x,y):
								self.collision(char, e)

	def activateSwitches(self):
		mp = self.currentMap()
		for s in mp.switches:
			x,y = mp.posToGrid(s.getPos())
			charPos = [self.currentMap().posToGrid(self.characters[char].getPos()) for char in self.characters]
			if mp.tiles[Map.COLLISION][y][x] != ' ' or ((x,y) in charPos):
				#print 'activated!'
				mp.tiles[Map.GROUND][y][x] = 'S'
				s.activate()
			else:
				#print 'deactivated!'
				mp.tiles[Map.GROUND][y][x] = 's'
				s.deactivate()

		for d in mp.doors:
			openDoor = True
			if d.openWith == "switches":
				for ds in d.switches:
					for ms in mp.switches:
						if (ds == ms.name) and (not ms.active):
							openDoor = False
							break
				if openDoor:
					d.open("switches")
					x,y = mp.posToGrid(d.getPos())
					mp.tiles[Map.COLLISION][y][x] = ' '

	def collision(self, a, b):
		print "Collision: TYPE A:", a.getType(), "TYPE B:", b.getType()

		if b.getType() == 'item':
			for i in range(len(self.currentMap().items)):
				if i < len(self.currentMap().items): #we need this because the size of the list may change if we remove an item
					if tuple(self.currentMap().items[i].getPos()) == tuple(b.getPos()):
						# removes the item
						self.currentMap().items.pop(i)

						x, y = self.currentMap().posToGrid((NodePath(b.getNode()).getX(), NodePath(b.getNode()).getZ()))

						# it's not drawed anymore
						self.currentMap().tiles[Map.COLLISION][y][x] = ' '
						NodePath(b.getNode()).detachNode()

						#it's picked
						oldItem = a.pickItem(b)
						if oldItem != None:
							print oldItem.name
							oldItem.setPos(self.currentMap().gridToPos((x,y)))
							oldItem.originalPos = oldItem.getPos()
							self.spawnObject(oldItem)
							self.currentMap().items.append(oldItem)

		if a.getType() == 'liftable' and b.getType() == 'enemy':
			a.stop()
			a.getNode().detachNode()
			x,y = self.currentMap().posToGrid(a.getPos()) #nao precisaria
			self.currentMap().tiles[Map.COLLISION][y][x] = ' '
			b.takeDamage(10000)

		if a.getType() == 'block' and b.getType() == 'enemy':
			b.takeDamage(10000)

		if a.getType() == 'Character':
			print("Character collided with", b.getType())
			if b.getType() == 'enemy':
				a.takeDamage(1)

	def buryDeadPeople(self):
		# commented while fixing the bugs
		for enemy in self.currentMap().enemies:
			if not enemy.isAlive():
				x, y = self.currentMap().posToGrid(enemy.getPos())
				self.currentMap().tiles[Map.COLLISION][y][x] = ' '
				NodePath(enemy.getNode()).removeNode()
				self.currentMap().enemies.remove(enemy)

		#if not self.player.isAlive() : #tratar isso corretamente!
		for char in self.characters:
			if not self.characters[char].isAlive():
				self.isOver = True

	def exit(self):

		self.stage.stopMusic()
		self.heartsNode.removeNode()
		for c in self.characters:
			NodePath(self.characters[c].getNode()).removeNode()
			self.status[c].removeNode()

		NodePath(self.currentMap().getNode()).removeNode()
		State.exit(self)


# to do (or not): create GameServer and GameClient classes to inherit from Game

