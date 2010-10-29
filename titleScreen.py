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
		
		menuActions = {'up': (Menu.previousOpt, self.menu),
						'down': (Menu.nextOpt, self.menu), 
						'action': (self.selectOption, None)}
						
		self.menu.registerKeys(keys, menuActions)
		
	def iterate(self):
		State.iterate(self)
		return self.menu.iterate()
		
	def selectOption(self, opt):
		return self.optState[self.menu.selected]