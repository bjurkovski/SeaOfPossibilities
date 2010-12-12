from panda3d.core import CardMaker, PandaNode, NodePath
from direct.gui.DirectGui import OnscreenText
from gameLoader import *
from state import *
from menu import *

class NewGame(State):
	def __init__(self):
		State.__init__(self)

		modeOptions = ['Single-Player', 'Multi-Player']
		self.optState = ['single', 'multi']

		self.menu = Menu()
		self.menu.addOptions(modeOptions)
		self.innerState = "Choosing Mode"

	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)

		cm = CardMaker('CardMaker-NewGame')
		#tex = loadTexture('titlescreen.png')

		cm.setFrame(-1, 1, -1, 1)

		self.bg = self.node.attachNewNode(cm.generate())
		self.bg.setPos(0, 0, 0)
		self.bg.setColor(0, 0, 0)
		#self.bg.setTexture(tex)

		menuActions = {'left': (Menu.previousOpt, self.menu),
						'right': (Menu.nextOpt, self.menu),
						'action': (self.selectOption, None)
						}

		self.menu.registerKeys(keys, menuActions)

		self.title = OnscreenText(text="Game Mode", mayChange = True , style=2, fg=(1,1,1,1), pos=(0, 0.75), scale = 0.15)
		self.text = {}

		id=0
		for opt in self.menu.options:
			self.text[opt] = OnscreenText(text=opt, mayChange = True , style=2, fg=(1,1,1,1), pos=(-0.5 + 1*id, -0.3), scale = .1)
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

		if self.innerState == "Choosing Mode":
			ret = self.menu.iterate()
			if ret != None:
				for opt in self.menu.options:
					self.text[opt].removeNode()
				self.title.setText("Choose Player")

				playerOptions = ['Jackson', 'Jackson2']
				self.menu.clearOptions()
				self.menu.addOptions(playerOptions)

				id = 0
				for opt in self.menu.options:
					self.text[opt] = OnscreenText(text=opt, mayChange = True , style=2, fg=(1,1,1,1), pos=(-0.5 + 1*id, -0.3), scale = .1)
					self.text[opt].reparentTo(self.node)
					id+=1

				if ret == "single":
					self.innerState = "Choosing Single"
				elif ret == "multi":
					self.innerState = "Choosing Multi"

			return None
		elif self.innerState == "Choosing Single":
			ret = self.menu.iterate()
			if ret != None:
				return 'InGame'
		elif self.innerState == "Choosing Multi":
			ret = self.menu.iterate()
			if ret != None:
				return 'InGame'

	def selectOption(self, opt):
		return self.optState[self.menu.selected]

