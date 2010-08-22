from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")


from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec2,Vec3,Vec4

from panda3d.core import CardMaker
from direct.gui.DirectGui import *

from stage import *

import sys


class MapEditor(ShowBase):
	def __init__(self, w, h):
		ShowBase.__init__(self)

		#Disable mouse-based camera-control
		base.disableMouse()

		#number of cells to be present in the map field
		self.width = w
		self.height = h

		self.map = Map(size=(w,h))
		
		# maybe store a "theme" attribute in map and apply the texture there
		tex = loader.loadTexture('tex/tile.png')
		for i in range(w):
			for j in range(h):
				self.map.cards[i][j].setTexture(tex)

		self.render2d.attachNewNode(self.map.getNode())

		self.mouse = (0,0)

		self.title = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.5,-0.95), scale = .07)

		taskMgr.add(self.mouseInput, "mouseInput")
		taskMgr.add(self.idle,"idle")

		self.accept('escape', sys.exit)


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

		return Task.cont



app = MapEditor(20,20)
app.run()

