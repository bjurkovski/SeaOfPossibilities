from panda3d.core import CardMaker, PandaNode, NodePath
from pandac.PandaModules import TransparencyAttrib

from gameLoader import *

class Sprite:
	cardMaker = CardMaker('CardMaker-Sprites')
	
	def __init__(self, filename, sizeX, sizeY):
		Sprite.cardMaker.setFrame(-sizeX/2.0, sizeX/2.0, -sizeY/2.0, sizeY/2.0)
		self.node = NodePath(Sprite.cardMaker.generate())
		self.node.setAttrib(TransparencyAttrib.make(TransparencyAttrib.MAlpha))

		tex = loadTexture(filename)
		self.node.setTexture(tex)

	def getNode(self):
		return self.node

	def setPos(self, x, y):
		self.node.setPos(x, 0, y)
