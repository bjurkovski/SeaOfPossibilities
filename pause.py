from panda3d.core import CardMaker, PandaNode, NodePath
from direct.gui.DirectGui import OnscreenText

from state import *
from menu import *

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
		options = ['Continue', 'Main Menu', 'Exit']
		
		self.menu = Menu()
		self.menu.addOptions(options)
		
		menuActions = {'up': (Menu.previousOpt, self.menu),
						'down': (Menu.nextOpt, self.menu), 
						'action': (self.selectOption, None),
						'cancel': (self.selectOption, 0) }
		self.menu.registerKeys(keys, menuActions)
	
		# Here we have the States in the FSM represented by the options
		self.optState = ['InGame', 'Title', 'Exit']
		self.title = OnscreenText(text="Game Paused", mayChange = True , style=1, fg=(1,1,1,1), pos=(0,0.35), scale = .1)
		self.text = {}
		
		id=0
		for opt in self.menu.options:
			self.text[opt] = OnscreenText(text=opt, mayChange = True , style=1, fg=(1,1,1,1), pos=(0,0.1 - 0.1*id), scale = .06)
			id+=1
		
		self.title.reparentTo(self.node)
		for opt in self.text.keys():
			self.text[opt].reparentTo(self.node)
		
	def iterate(self):
		State.iterate(self)
		self.camera.look()
		
		for option in self.text.keys():
			self.text[option].setScale(0.06)
		self.text[self.menu.options[self.menu.selected]].setScale(0.08)
		
		return self.menu.iterate()
		
	def selectOption(self, param):
		if param==None:
			return self.optState[self.menu.selected]
		else:
			return self.optState[param]