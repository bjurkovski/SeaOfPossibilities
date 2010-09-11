from panda3d.core import CardMaker, PandaNode, NodePath
from direct.gui.DirectGui import OnscreenText

from state import *

class Pause(State):
	def __init__(self):
		State.__init__(self)
		
	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)
		
		cm = CardMaker('CardMaker-Pause')
		cm.setFrame(0.5, -0.5, 0.5, -0.5)
		cm.setColor(0,0,0, 0.1)
		
		self.bg = self.node.attachNewNode(cm.generate())
		self.bg.setPos(0, 0, 0)
		
		# Options in the Pause Menu
		self.options = ['Continue', 'Main Menu', 'Exit']
		# Here we have the States in the FSM represented by the options
		self.optState = ['InGame', 'Title', 'Exit']
		self.title = OnscreenText(text="Game Paused", mayChange = True , style=1, fg=(1,1,1,1), pos=(0,0.35), scale = .1)
		self.text = {}
		
		id=0
		for option in self.options:
			self.text[option] = OnscreenText(text=option, mayChange = True , style=1, fg=(1,1,1,1), pos=(0,0.1 - 0.1*id), scale = .06)
			id+=1
		
		self.selected = 0
		self.title.reparentTo(self.node)
		for option in self.text.keys():
			self.text[option].reparentTo(self.node)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()
		
		for option in self.text.keys():
			self.text[option].setScale(0.06)
		self.text[self.options[self.selected]].setScale(0.08)
		
		if self.keys['up']:
			self.selected = (self.selected + len(self.options) - 1)%len(self.options)
		elif self.keys['down']:
			self.selected = (self.selected +  1)%len(self.options)
		elif self.keys['action']:
			return self.optState[self.selected]
		elif self.keys["cancel"]:
			return "InGame"
		