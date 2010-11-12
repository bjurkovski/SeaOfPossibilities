from state import *
from character import *
from stage import *
from item import *
from player import *

import sys

from direct.actor.Actor import Actor
from panda3d.core import Point2, Point3
from panda3d.core import LightRampAttrib

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

		# initialize character status string
		self.statusString = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.7,-0.75), scale = .08)


	def spawnObject(self, ob, ob_type):

		if ob_type == "enemy":
			ob["instance"] = Character("char/" + ob["name"])
			self.players.append( ComputerPlayer(ob["instance"]) )

		elif ob_type == "item":
			#instance is ready when we have an item
			# This is not what it looks like, I can explain!			
			ob["instance"].extra = ob

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
		elif direction == "down":    y = 1
		elif direction == "up":  y = map.height-2
		pos = self.currentMap().gridToPos((x,y))
		self.characters[self.player].setPos(pos)
		
		self.startMap()
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		self.node.attachNewNode(self.stage.maps[self.room].getNode())

		char = self.characters[self.player]
		self.players.append( HumanPlayer( char , keys ) )
		
		char2 = self.characters[self.player2]
		self.players.append(HumanPlayer( char2 , keys ))
		
		for char in self.characters.values():
			char.getNode().reparentTo(self.node)
			
		for l in self.stage.getLights():
			render.setLight(l)
			
		#COWABUNGA comment this to stop the madness
		render.setAttrib(LightRampAttrib.makeSingleThreshold(0.1, 1))
		#render.setAttrib(LightRampAttrib.makeDoubleThreshold(0.1, 0.3, 0.9 , 1))

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
				char.stop()
				x, y = self.currentMap().posToGrid(char.getCollisionPos(char.direction))
				# BLOCK MOVEMENT TRIGGER
				if self.keys["action"+add] and self.stage.maps[self.room].tileIs(1, (x,y), 'block'):
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
							print('sai da frente satanas')

					if self.stage.maps[self.room].tileIs(1, (x,y), 'item'):
						for item in self.currentMap().items:
							if tuple(item["pos"]) == (x,y):
								self.collision(char, item['instance'])
					
					elif self.stage.maps[self.room].tileIs(1, (x,y), 'enemy'):
						for enemy in self.currentMap().enemies:
							if tuple(enemy["pos"]) == (x,y):
								self.collision(char, enemy["instance"])

				except Exception as e:
					print(e)
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


	def sendCommands(self):
		try:
			for player in self.players :
				player.sendCommand()
		except Exception as e:
			print(e)
			pass
	
	def processActions(self):
		try:
			for char in self.characters.values():
				#char = self.characters[char]
				#1st Step: Process movements
				for dir in char.tryToMove :
					try:
						print(dir)
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
						
						elif self.stage.maps[self.room].tileIs(1, (x,y), 'enemy'):
							for enemy in self.currentMap().enemies:
								if tuple(enemy["pos"]) == (x,y):
									self.collision(self.characters[self.player], enemy["instance"])
					except Exception as e:
						print(e.message)
						pass
				#2nd Step: Process actions
				#TODO
			
			for char in self.currentMap().enemies:
				char = char["instance"]
				#1st Step: Process movements
				for dir in char.tryToMove :
					try:
						print(dir)
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
						
						elif self.stage.maps[self.room].tileIs(1, (x,y), 'enemy'):
							for enemy in self.currentMap().enemies:
								if tuple(enemy["pos"]) == (x,y):
									self.collision(self.characters[self.player], enemy["instance"])
					except Exception as e:
						print(e)
						pass
				#2nd Step: Process actions
				#TODO
		except Exception as e:
			print(e)
			pass
# to do (or not): create GameServer and GameClient classes to inherit from Game

