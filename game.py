from state import *

from stage import *

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

	def currentMap(self):
		return self.stage.maps[self.room]

	def changeMap(self,direction):
		NodePath(self.currentMap().getNode()).detachNode()
		self.room = self.stage.doors[self.room][direction]
		NodePath(self.currentMap().getNode()).reparentTo(render)
		
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
		self.characters[self.player].getNode().setPos(pos[0], 0, pos[1])
	
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
		
		if self.keys['start']:
			return "Paused"

	def move(self):
		directions = [key for key in ["up","down","left","right"] if self.keys[key]]
		
		self.characters[self.player].stop()
		
		hprs = {"up": (0,0,180),
				"left": (0,0,90),
				"down": (0,0,0),
				"right": (0,0,270)}
		
		disp = {"up": Point3(0, 0, self.characters[self.player].speed),
				"left": Point3(-self.characters[self.player].speed, 0, 0),
				"down": Point3(0, 0, -self.characters[self.player].speed),
				"right": Point3(self.characters[self.player].speed, 0, 0)}
			
		#if self.stage.maps[self.room].tileIs((x+Game.mapOffset[dir][0],y+Game.mapOffset[dir][1]), 'ground'):
		
		for dir in directions:
			try:
				x, y = self.posToGrid((self.characters[self.player].model.getX()+disp[dir].getX(), self.characters[self.player].model.getZ()+disp[dir].getZ()))
				#mudar o "ground" pra "free" ou algo do genero depois
				#print "t:",x,y
				if self.stage.maps[self.room].tileIs((x,y), 'ground'):
					self.characters[self.player].displacement += disp[dir]
					
				# ESSA PARTE TA BUGADA PQ TAMOS CONSIDERANDO QUE O MOVIMENTO DO PERSONAGEM EH DISCRETO
				# MAS NA VERDADE EH CONTINUO... ARRUMAR ISSO!!!
				#if self.stage.maps[self.room].tileIs((x+Game.mapOffset[dir][0],y+Game.mapOffset[dir][1]), 'ground'):
				#	self.characters[self.player].doAction("walk", [dir])
				#	x += Game.mapOffset[dir][0]
				#	y += Game.mapOffset[dir][1]
			except IndexError:
				pass
		
		self.characters[self.player].doAction("walk")
		x, y = self.posToGrid((self.characters[self.player].model.getX(), self.characters[self.player].model.getZ()))
		ex = self.stage.maps[self.room].getExit((x,y))
		
		print x,y,ex
		if ex and (ex in self.stage.doors[self.room].keys()):
			self.changeMap(ex)

	def collision(self, a, b):
		#if b.getType() == 'mine':
		#	a.takeDamage()
		if a.getType() == 'player':
			if b.getType() == 'rock':
				a.stop()
			#if b.getType() == 'enemy':
				#a.takeDamage()
			#if b.getType() == 'item':
				#testa se a quer pegar item (e em caso positivo, pega)
			#(...)
		#elif a.getType() == 'enemy'
	

# to do (or not): create GameServer and GameClient classes to inherit from Game

