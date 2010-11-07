from state import *
from character import *
from stage import *
from item import *

import sys

from direct.actor.Actor import Actor
from panda3d.core import Point2, Point3
from panda3d.core import LightRampAttrib

class Game(State):
	mapOffset = {"up": (0,1), "down": (0,-1), "left": (-1,0), "right": (1,0)}
	def __init__(self, stage, characters, player):
		State.__init__(self)

		# how to know the players that will be in game? a ChoosePlayer screen before the constructor?
		self.itens = Item("cfg/itens.json")
		self.characters = characters
		self.player = player
		self.stage = stage
		self.room = self.stage.start
		self.isOver = False
		
		#let's try
		self.characters[self.player].drawStatus()
		
		self.startMap()

	def spawnObject(self, ob, ob_type):

		if ob_type == "enemy":
			ob["instance"] = Character("char/" + ob["name"])

		elif ob_type == "item":
			ob["instance"] = Model( self.itens.getModel(ob["name"]) )

		ob["instance"].getNode().reparentTo(NodePath(self.currentMap().getNode()))
		pos = self.currentMap().gridToPos(ob["pos"])
		ob["instance"].setPos(pos)
		ob["instance"].type =  ob_type
		self.currentMap().tiles[1][ob["pos"][1]][ob["pos"][0]] = ob_type[0] #TODO fix this... if you try hard you can see why it works , to be refactored

	def currentMap(self):
		return self.stage.maps[self.room]
		
	def exitMap(self):
		NodePath(self.currentMap().getNode()).detachNode()

	def startMap(self):
		if not self.currentMap().started:
			for obstacle in self.currentMap().obstacles:
				self.spawnObject(obstacle,'obstacle')

			for enemy in self.currentMap().enemies:
				self.spawnObject(enemy,'enemy')
			
			for item in self.currentMap().items:
				self.spawnObject(item,'item')

			for block in self.currentMap().blocks:
				self.spawnObject(block,'block')

			self.currentMap().started = True

	def changeMap(self,direction):
		self.exitMap()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(self.node)
		
		map = self.stage.maps[self.room]
		x, y = self.currentMap().posToGrid(self.characters[self.player].getPos())
		if   direction == "right": x = 1
		elif direction == "left":  x = map.width-2
		elif direction == "up":    y = 1
		elif direction == "down":  y = map.height-2
		pos = self.currentMap().gridToPos((x,y))
		self.characters[self.player].setPos(pos)
		
		self.startMap()
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())
		
		for char in self.characters.values():
			char.getNode().reparentTo(self.node)
			
		for l in self.stage.getLights():
			render.setLight(l)
			
		#COWABUNGA comment this to stop the madness
		#render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 1))
		#render.setAttrib(LightRampAttrib.makeDoubleThreshold(0.1, 0.3, 0.9 , 1))

		self.camera.setPos(0, -2.5, -2.5)
		self.camera.lookAt(0, 0, 0)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()

		self.move()
		self.buryDeadPeople()
		
		if self.isOver:
			return "GameOver"
		elif self.keys['start']:
			return "Paused"

	def move(self):		
		directions = [key for key in ["up","down","left","right"] if self.keys[key]]
		char = self.characters[self.player]
		
		# I know the block movement code sucks by now... i was just testing it and will refactor
		
		# BLOCK MOVEMENT ACTION
		for block in self.currentMap().blocks:
			if block["instance"].isMoving:
				x,y = self.currentMap().posToGrid(block["instance"].getPos())
				bx, by = self.currentMap().posToGrid(block["instance"].getCollisionPos(block["instance"].direction))
				if (x,y)==(bx,by) or self.stage.maps[self.room].tileIs(1, (bx,by), 'free'):
					block["instance"].move(block["instance"].direction)
					self.currentMap().tiles[1][block["pos"][1]][block["pos"][0]] = ' '
					block["pos"] = self.currentMap().posToGrid(block["instance"].getPos())
					self.currentMap().tiles[1][block["pos"][1]][block["pos"][0]] = 'b'
				else:
					block["instance"].stop()
		
		if len(directions) == 0:
			self.characters[self.player].stop()
			x, y = self.currentMap().posToGrid(char.getCollisionPos(char.direction))
			# BLOCK MOVEMENT TRIGGER
			if self.keys["action"] and self.stage.maps[self.room].tileIs(1, (x,y), 'block'):
				for block in self.currentMap().blocks:
					if tuple(block["pos"]) == (x,y):
						bx, by = self.currentMap().posToGrid(block["instance"].getCollisionPos(char.direction))
						if self.stage.maps[self.room].tileIs(1, (bx,by), 'free'):
							block["instance"].move(char.direction)
							self.currentMap().tiles[1][block["pos"][1]][block["pos"][0]] = ' '
							block["pos"] = self.currentMap().posToGrid(block["instance"].getPos())
							self.currentMap().tiles[1][block["pos"][1]][block["pos"][0]] = 'b'
		
		for dir in directions:
			try:
				#TODO to be re-refactored
				x, y = self.currentMap().posToGrid(char.getCollisionPos(dir))

				if self.stage.maps[self.room].tileIs(1, (x,y), 'free'):
					char.move(dir)
					ex = self.stage.maps[self.room].getExit((x,y))		
					if ex and (ex in self.stage.doors[self.room].keys()):
						self.changeMap(ex)
				else:
					char.setDirection(dir)
					
				if self.stage.maps[self.room].tileIs(1, (x,y), 'item'):
					for item in self.currentMap().items:
						if tuple(item["pos"]) == (x,y):
							self.collision(self.characters[self.player], item["instance"])
				#elif self.stage.maps[self.room].tileIs(1, (x,y), 'block'):
				#	for block in self.currentMap().blocks:
				#		if tuple(block["pos"]) == (x,y):
				#			self.collision(self.characters[self.player], block["instance"])
				#			block["pos"] = self.currentMap().posToGrid(block["instance"].getPos())
				elif self.stage.maps[self.room].tileIs(1, (x,y), 'enemy'):
					for enemy in self.currentMap().enemies:
						if tuple(enemy["pos"]) == (x,y):
							self.collision(self.characters[self.player], enemy["instance"])
			except IndexError:
				pass

	def collision(self, a, b):
		print "TYPE A:", a.getType(), "TYPE B:", b.getType()
		if b.getType() == 'item':
		
			for i in range(len(self.currentMap().items)):
				if tuple(self.currentMap().items[i]["instance"].getPos()) == tuple(b.getPos()):
					self.currentMap().items.pop(i)
					x, y = self.currentMap().posToGrid((NodePath(b.getNode()).getX(), NodePath(b.getNode()).getZ()))
					self.currentMap().tiles[1][y][x] = ' '
					NodePath(b.getNode()).removeNode()

		if a.getType() == 'Character':
			print("Collided with", b.getType())
			if b.getType() == 'enemy':
				if len(self.currentMap().items) == 0:
					b.takeDamage(10)
				else:
					a.takeDamage(10)
			if b.getType() == 'block':
				x ,y = self.currentMap().posToGrid(b.getPos())
				disp = a.oldDisplacement
				fx,fy = self.currentMap().posToGrid(b.getPos() + disp*10)
				if self.stage.maps[self.room].tileIs(1, (fx,fy), 'free'):
					b.setPos(b.getPos() + disp*10)
					self.currentMap().tiles[1][y][x] = ' '
					self.currentMap().tiles[1][fy][fx] = 'b'

	def buryDeadPeople(self):
		for enemy in self.currentMap().enemies:
			if not enemy["instance"].isAlive():
				x, y = self.currentMap().posToGrid(NodePath(enemy["instance"].getNode()).getPos())
				self.currentMap().tiles[1][y][x] = ' '
				NodePath(enemy["instance"].getNode()).removeNode()
				self.currentMap().enemies.remove(enemy)
				#self.currentMap().enemies.pop(e)

		#if not self.player.isAlive() : #tratar isso corretamente!
		for char in self.characters:
			if not self.characters[char].isAlive():
				self.isOver = True



# to do (or not): create GameServer and GameClient classes to inherit from Game

