from state import *
from menu import *
from gameLoader import *

from panda3d.core import CardMaker, PandaNode, NodePath

class GameOver(State):
	def __init__(self):
		State.__init__(self)

	def register(self, render, camera, keys):
		State.register(self, render, camera, keys)

	def iterate(self):
		cm = CardMaker('CardMaker-GameOver')
		tex = loadTexture('gameover.png')

		cm.setFrame(-1, 1, -1, 1)
		bg = self.node.attachNewNode(cm.generate())
		bg.setColor(0, 0, 0)
		bg.setPos(0, 0, 0)

		cm.setFrame(-0.4, 0.4, -0.2, 0.2)
		self.text = self.node.attachNewNode(cm.generate())
		self.text.setPos(0, 0, 0)
		self.text.setTexture(tex)

