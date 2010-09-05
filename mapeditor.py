from pandac.PandaModules import loadPrcFileData
#loadPrcFileData("", "want-directtools #t")
#loadPrcFileData("", "want-tk #t")


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Vec2,Vec3,Vec4

from panda3d.core import CardMaker,NodePath,PandaNode
from direct.gui.DirectGui import *

from gameLoader import *
from stage import *

import sys

class MapEditor(ShowBase):
	def __init__(self, w, h):
		ShowBase.__init__(self)
		
		self.mapNode = NodePath(PandaNode("map"))
		
		self.loader = GameLoader()
		self.loadStuff()

		#number of cells to be present in the map field
		self.width = w
		self.height = h

		self.map = Map( size=(w,h) )

		# maybe store a "theme" attribute in map and apply the texture there
#		tex = self.loader["textures"]["tile.png"]
#		for i in range(w):
#			for j in range(h):
#				self.map.cards[i][j].setTexture(tex)

		self.mapNode.reparentTo(render)

		self.mouse = (0,0)

		self.title = OnscreenText(mayChange= True , style=1, fg=(1,1,1,1), pos=(0.5,-0.95), scale = .07)

		self.addTasks()

	def addTasks(self):
		taskMgr.add(self.mouseInput, "mouseInput")
		taskMgr.add(self.idle,"idle")
		self.accept('escape', sys.exit)

	def loadStuff(self):
		self.loader.loadTexture("tile.png")
		self.loader.loadTexture("tree.png")
		self.loader.loadTexture("rock.png")

	def mouseInput(self,task):
		if base.mouseWatcherNode.hasMouse():
			sx, sy =  2.0/self.width , 2.0/self.height
			m = base.mouseWatcherNode.getMouse()
			self.mouse = ( int ( (m.getX()+1)//sx ) , int ( (m.getY()+1)//sy ) )

		return task.cont

	def idle(self, task):
		self.camera.setPos(0, -10, 10)
		self.camera.lookAt((0,0,0) ,(0,0,1))
		self.title.setText ("MapMaker (%02d,%02d)" % ( self.mouse[0], self.mouse[1] ) )
		
		return task.cont



app = MapEditor(20,20)
app.run()

