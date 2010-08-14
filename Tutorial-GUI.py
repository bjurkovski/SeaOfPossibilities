from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import CardMaker
from direct.gui.DirectGui import *
 
class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		self.cm = CardMaker('card')
		self.cm.setFrame(0.8,-0.8,0.8,-0.8)
		self.cm.setColor(0,1,0,1)
		# usando render2d, tudo que for desenhado vai ser desenhado como se fosse pintado na lente da camera
		# (em cima de todo o resto ja desenhado). Coordenadas da tela no range [-1,1]
		self.card = self.render2d.attachNewNode(self.cm.generate())
		# eh possivel usar o render padrao (3d) tambem, mas dai seria necessario usar o TaskManager (vide abaixo)
		#self.card = self.render2d.attachNewNode(self.cm.generate())
		tex = loader.loadTexture('map.png')
		self.card.setTexture(tex)

		# usando o render padrao (3d), eh necessario adicionar esse callback
		# Aparentemente esse eh o segredo pra mostrar o Card na tela, mas nao descobri o pq...
		#self.taskMgr.add(self.idle, "Idle")

		self.title = OnscreenText(text="MapMaker",
								  style=1, fg=(1,1,1,1),
								  pos=(0.5,-0.95), scale = .07)

	def idle(self, task):
		#se colocar esse setPos no __init__, nao funciona...
		self.camera.setPos(0, -20.0, 0)
		return Task.cont
 
app = MyApp()
app.run()
