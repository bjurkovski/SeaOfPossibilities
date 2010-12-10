from panda3d.core import CardMaker, PandaNode, NodePath
from direct.gui.DirectGui import OnscreenText
from gameLoader import *
from state import *
from menu import *

class TitleScreen(State):
	def __init__(self):
		State.__init__(self)

		options = ['New Game', 'Options', 'Exit']
		self.optState = ['InGame', 'Options', 'Exit']

		self.menu = Menu()
		self.menu.addOptions(options)

	def register(self, render, camera, keys):

		State.register(self, render, camera, keys)


		cm = CardMaker('CardMaker-Title')
		cm.setFrame(1, -1, 1, -1)
		cm.setColor(0,0,0, 0.5)

		self.bg = self.node.attachNewNode(cm.generate())
		self.bg.setPos(0, 0, 0)

		menuActions = {'up': (Menu.previousOpt, self.menu),
						'down': (Menu.nextOpt, self.menu),
						'action': (self.selectOption, None)
						}

		self.menu.registerKeys(keys, menuActions)

		self.title = OnscreenText(text="Sea of Possibilities", mayChange = True , style=2,
							 fg=(1,1,1,1), pos=(0,0.75), scale = 0.2)
		self.text = {}

		id=0
		for opt in self.menu.options:
			self.text[opt] = OnscreenText(text=opt, mayChange = True , style=1, fg=(1,1,1,1), pos=(0,0.1 - 0.1*id), scale = .1)
			id+=1

		self.title.reparentTo(self.node)
		for opt in self.text.keys():
			self.text[opt].reparentTo(self.node)


		State.register(self, render, camera, keys)


	def iterate(self):
		State.iterate(self)
		self.camera.look()

		for option in self.text.keys():
			self.text[option].setScale(0.1)
		self.text[self.menu.options[self.menu.selected]].setScale(0.12)

		return self.menu.iterate()

	def selectOption(self, opt):
		return self.optState[self.menu.selected]

