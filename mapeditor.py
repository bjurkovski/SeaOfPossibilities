from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")


from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec2,Vec3,Vec4

from panda3d.core import CardMaker
from direct.gui.DirectGui import *

import sys

def line(w,default=None):
	lin = []
	for i in range(w):
		lin.append(default)

	return lin

def matrix(w,h,default=None):
	mat = []
	for i in range(w):
		mat.append( line(h,default) )

	return mat


class MyApp(ShowBase):

	def __init__(self, w, h):
		ShowBase.__init__(self)

		#Disable mouse-based camera-control
		base.disableMouse()

		#number of cells to be present in the map field
		self.width = w
		self.height = h

		#the card generator
		self.cardMaker = CardMaker('card')

		self.fillMatrix()

		self.mouse = (0,0)

		self.title = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.5,-0.95), scale = .07)

		taskMgr.add(self.mouseInput, "mouseInput")
		taskMgr.add(self.idle,"idle")

		self.accept('escape', sys.exit)

	def drawBoard(self):
		self.matrix[self.mouse[0]][self.mouse[1]].setColor(0,0,0,1)

	def fillMatrix(self):
		self.matrix = matrix(self.width,self.height)
		tex = loader.loadTexture('tex/tile.png')

		for i in range(self.width):
			for j in range(self.height):
				sx, sy =  2.0/self.width , 2.0/self.height
				card = self.render2d.attachNewNode( self.newCard(sx,sy) )
				card.setPos( sx/2 + i*sx - 1 , 0, sy/2 + j*sy - 1)
				card.setTexture(tex)
				self.matrix[i][j] = card

	def newCard( self, w, h ):
		self.cardMaker.setFrame(w/2,-w/2,h/2,-h/2)
		self.cardMaker.setColor(0,0.5,0,1)
		return self.cardMaker.generate()

	def mouseInput(self,task):

		if base.mouseWatcherNode.hasMouse():
			sx, sy =  2.0/self.width , 2.0/self.height
			m = base.mouseWatcherNode.getMouse()
			self.mouse = ( int ( (m.getX()+1)//sx ) , int ( (m.getY()+1)//sy ) )

		return Task.cont

	def idle(self, task):
		#se colocar esse setPos no __init__, nao funciona...
		#self.camera.setPos(0, 0, 0)
		self.title.setText ("MapMaker (%02d,%02d)" % ( self.mouse[0], self.mouse[1] ) )
		self.drawBoard()
		return Task.cont



app = MyApp(20,20)
app.run()

