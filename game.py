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
		x = int(pos[0] / (map.squareWidth) + map.width/2)
		y = int(pos[1] / (map.squareHeight) + map.height/2)
		
		return (x,y)
	
	def gridToPos(self, grid):
		map = self.stage.maps[self.room]
		x = (grid[0] - map.width/2) * map.squareWidth
		y = (grid[1] - map.height/2) * map.squareHeight
		
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
		x, y = self.posToGrid((self.characters[self.player].model.getX(), self.characters[self.player].model.getZ()))
		directions = [key for key in ["up","down","left","right"] if self.keys[key]]
		
		for dir in directions:
			try:
				#mudar o "ground" pra "free" ou algo do genero depois
				
				# ESSA PARTE TA BUGADA PQ TAMOS CONSIDERANDO QUE O MOVIMENTO DO PERSONAGEM EH DISCRETO
				# MAS NA VERDADE EH CONTINUO... ARRUMAR ISSO!!!
				if self.stage.maps[self.room].tileIs((x+Game.mapOffset[dir][0],y+Game.mapOffset[dir][1]), 'ground'):
					self.characters[self.player].doAction("walk", [dir])
					x += Game.mapOffset[dir][0]
					y += Game.mapOffset[dir][1]
			except IndexError:
				pass
		
		ex = self.stage.maps[self.room].getExit((x,y))
		
		print x,y,ex
		if ex and (ex in self.stage.doors[self.room].keys()):
			self.changeMap(ex)

			

# to do (or not): create GameServer and GameClient classes to inherit from Game

