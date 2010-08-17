from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")


from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import CardMaker
from direct.gui.DirectGui import *

class MyApp(ShowBase):

	def __init__(self, w, h):
		ShowBase.__init__(self)

		#number of cells to be present in the map field

		self.width = w
		self.height = h

		#the card generator
		self.cardMaker = CardMaker('card')

		tex = loader.loadTexture('tex/tile.png')
		for i in range(self.width):
			for j in range(self.height):
				sx, sy =  1.0/self.width , 1.0/self.height
				card = self.render2d.attachNewNode( self.newCard(sx,sy) )
				card.setPos( (sx - 1 - (2*i*sx)) ,0, -(sy - 1 - (2 * j * sy)) )
				print( 1 - 2 * i * sx ,1 - 2 * j * sy ) 
				card.setTexture(tex)


		self.title = OnscreenText(text="MapMaker", style=1, fg=(1,1,1,1), pos=(0.5,-0.95), scale = .07)


	def newCard( self, w, h ):
		self.cardMaker.setFrame(w,-w,h,-h)
		self.cardMaker.setColor(0,1,0,1)
		return self.cardMaker.generate()

	def idle(self, task):
				
		#se colocar esse setPos no __init__, nao funciona...
		self.camera.setPos(0, 0, 0)
		return Task.cont



app = MyApp(20,20)
app.run()

