from state import *
from character import *
from stage import *

import sys

from direct.actor.Actor import Actor
from panda3d.core import Point3

class Game(State):
	mapOffset = {"up": (0,1), "down": (0,-1), "left": (-1,0), "right": (1,0)}
	def __init__(self, stage, characters, player):
		State.__init__(self)

		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.characters = characters
		self.player = player
		self.stage = stage
		self.room = self.stage.start
		
		self.startMap()

	def spawnObject(self, ob):
		if ob["name"] == "enemy":
			ob["instance"] = Character(ob["file"])
		else:
			ob["instance"] = Model(ob["model"])

		ob["instance"].getNode().reparentTo(NodePath(self.currentMap().getNode()))
		pos = ob["pos"]
		pos = self.gridToPos(pos)
		ob["instance"].getNode().setPos(pos[0], ob["instance"].getNode().getY(), pos[1])
		ob["instance"].type =  ob["name"]
		self.currentMap().tiles[1][ob["pos"][1]][ob["pos"][0]] = ob["symbol"]

	def currentMap(self):
		return self.stage.maps[self.room]
		
	def exitMap(self):
		NodePath(self.currentMap().getNode()).detachNode()

	def startMap(self):
		if not self.currentMap().started:
			for obstacle in self.currentMap().obstacles:
				self.spawnObject(obstacle)

			for enemy in self.currentMap().enemies:
				self.spawnObject(enemy)
			
			for item in self.currentMap().items:
				self.spawnObject(item)

			for block in self.currentMap().blocks:
				self.spawnObject(block)

			self.currentMap().started = True

	def changeMap(self,direction):
		self.exitMap()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(self.node)
		
		map = self.stage.maps[self.room]
		x, y = self.posToGrid((self.characters[self.player].model.getX(), self.characters[self.player].model.getZ()))
		if direction == "right":
			x = 1
		elif direction == "left":
			x = map.width-2
		elif direction == "up":
			y = 1
		elif direction == "down":
			y = map.height-2
		pos = self.gridToPos((x,y))
		self.characters[self.player].getNode().setPos(pos[0], self.characters[self.player].getNode().getY(), pos[1])
		
		self.startMap()
	
	# Conversion functions, maybe we should find a better place to put them...
	def posToGrid(self, pos):
		map = self.stage.maps[self.room]
		x = int((pos[0] + map.squareWidth/2) / (map.squareWidth) + map.width/2)
		y = map.height - int((pos[1] + map.squareHeight/2) / (map.squareHeight) + map.height/2) - 1
		
		return (x,y)
	
	def gridToPos(self, grid):
		map = self.stage.maps[self.room]
		#x = (grid[0] - map.width/2) * map.squareWidth
		x = (grid[0] + map.squareWidth/2 - map.width/2) * map.squareWidth
		#y = -(grid[1] - map.height/2 + 1) * map.squareHeight
		y = -(grid[1] + map.squareHeight/2 - map.height/2 + 1) * map.squareHeight
		
		return (x,y)
	# end of conversion functions ###############################################
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())
		for char in self.characters.values():
			char.getNode().reparentTo(self.node)
		
		self.camera.setPos(0, -3, -3)
		self.camera.lookAt(0, 0, 0)
		
		# to draw the item
		#cm = CardMaker('CardMaker')
		#cm.setFrame(0.2, 0, 0.2, 0)
		#card = self.nodePath.attachNewNode(cm.generate())
		#card.setPos((self.squareWidth/2 + x*self.squareWidth - 1), 0, -(self.squareHeight/2 + y*self.squareHeight - 1))
		#card.setTexture(tex)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()
		self.camera.camera.setPos(0, -3, -3)
		self.camera.camera.lookAt(0, 0, 0)
		self.move()
		self.buryDeadPeople()

		if self.keys['start']:
			return "Paused"

	def move(self):
		hprs = {"up": (0,0,180),
				"left": (0,0,90),
				"down": (0,0,0),
				"right": (0,0,270)}
		
		disp = {"up": Point3(0, 0, self.characters[self.player].speed),
				"left": Point3(-self.characters[self.player].speed, 0, 0),
				"down": Point3(0, 0, -self.characters[self.player].speed),
				"right": Point3(self.characters[self.player].speed, 0, 0)}
		
		directions = [key for key in ["up","down","left","right"] if self.keys[key]]
		
		self.characters[self.player].stop()
		
		for dir in directions:
			try:
				x, y = self.posToGrid((self.characters[self.player].model.getX()+disp[dir].getX(), self.characters[self.player].model.getZ()+disp[dir].getZ()))
				#mudar o "ground" pra "free" ou algo do genero depois
				#print "t:",x,y
				if self.stage.maps[self.room].tileIs(1, (x,y), 'free'):
					self.characters[self.player].displacement += disp[dir]
				elif self.stage.maps[self.room].tileIs(1, (x,y), 'item') :
					for item in self.currentMap().items:
						if item["pos"][0] == x and item["pos"][1] == y :
							self.collision(self.characters[self.player] , item["instance"])
							pass

				elif self.stage.maps[self.room].tileIs(1, (x,y), 'block'):
					for block in self.currentMap().blocks:
						if block["pos"][0] == x and block["pos"][1] == y:
							self.collision(self.characters[self.player] , block["instance"])
							node =  block["instance"].getNode()
							block["pos"] = self.posToGrid( (node.getX(),node.getZ()) )

				elif self.stage.maps[self.room].tileIs(1, (x,y), 'enemy') :
					for enemy in self.currentMap().enemies:
						if enemy["pos"][0] == x and enemy["pos"][1] == y :
							self.collision(self.characters[self.player] , enemy["instance"])
							pass
					
				#if not self.stage.maps[self.room].segundaCamadaIs((x,y), None) : 
				#	self.collision(self.characters[self.player], outro_mano)
			except IndexError:
				pass
				
		#ISSO (ABAIXO) NAO FAZ SENTIDO, MAS VAI FUNCIONAR PRA AMANHA!!!!!!!!! (move inimigo)
		for e in self.currentMap().enemies:
			e["instance"].stop()
			try:
				x, y = self.posToGrid((e["instance"].model.getX()+disp["up"].getX(), e["instance"].model.getZ()+disp["up"].getZ()))
				#mudar o "ground" pra "free" ou algo do genero depois
				#print "t:",x,y
				if self.stage.maps[self.room].tileIs(1, (x,y), 'free'):
					e["instance"].displacement += disp[dir]
					
				#if not self.stage.maps[self.room].segundaCamadaIs((x,y), None) : 
				#	self.collision(self.characters[self.player], outro_mano)
			except IndexError:
				pass
			e["instance"].doAction("walk")
		
		self.characters[self.player].doAction("walk")
		x, y = self.posToGrid((self.characters[self.player].model.getX(), self.characters[self.player].model.getZ()))
		ex = self.stage.maps[self.room].getExit((x,y))
		
		if ex and (ex in self.stage.doors[self.room].keys()):
			self.changeMap(ex)

	def collision(self, a, b):
		print "TYPE A:", a.getType(), "TYPE B:", b.getType()
		if b.getType() == 'mine':
		
			for i in range(len(self.currentMap().items)):
				if NodePath(self.currentMap().items[i]["instance"].getNode()).getX() == NodePath(b.getNode()).getX() and NodePath(self.currentMap().items[i]["instance"].getNode()).getZ() == NodePath(b.getNode()).getZ():
					self.currentMap().items.pop(i)
					x, y = self.posToGrid((NodePath(b.getNode()).getX(), NodePath(b.getNode()).getZ()))
					self.currentMap().tiles[1][y][x] = ' '
					NodePath(b.getNode()).removeNode()

		if a.getType() == 'Charlie':
			print("Collided with", b.getType())
			#if b.getType() == 'rock':
				#a.stop()
			if b.getType() == 'enemy':
				if len(self.currentMap().items) == 0:
					b.takeDamage(10)
				else:
					a.takeDamage(10)
			#(...)
			if b.getType() == 'block':
				#TODO refactor this
				x ,y = self.posToGrid( (b.getNode().getX(), b.getNode().getZ()) )
				disp = a.old_displacement
				node = b.getNode()
				self.currentMap().tiles[1][y][x] = ' '
				node.setPos(node.getPos() + disp*10)
				x ,y = self.posToGrid( (b.getNode().getX(), b.getNode().getZ()) )
				self.currentMap().tiles[1][y][x] = 'b'
				#empurrar

	def buryDeadPeople(self):
		for enemy in self.currentMap().enemies:
			if not enemy["instance"].isAlive():
				x, y = self.posToGrid((NodePath(enemy["instance"].getNode()).getX(), NodePath(enemy["instance"].getNode()).getZ()))
				self.currentMap().tiles[1][y][x] = ' '
				NodePath(enemy["instance"].getNode()).removeNode()
				self.currentMap().enemies.remove(enemy)

		#if not self.player.isAlive() : #tratar isso corretamente!
		for char in self.characters:
			if not self.characters[char].isAlive():
				#self.characters.remove(char)
				print "Game Over!"
				sys.exit()

# to do (or not): create GameServer and GameClient classes to inherit from Game

