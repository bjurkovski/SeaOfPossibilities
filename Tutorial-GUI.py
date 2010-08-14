from direct.directbase import DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import CardMaker
from panda3d.core import TextNode
import sys, os

title = OnscreenText(text="MapMaker",
                       style=1, fg=(1,1,1,1),
                       pos=(0.5,-0.95), scale = .07)

cm = CardMaker('card')
cm.setFrame(1,-1,1,-1)
cm.setColor(0,1,0,0)
card = render.attachNewNode(cm.generate())

tex = loader.loadTexture('map.png')
card.setTexture(tex)

#geom.setFrameFullscreenQuad(-1,1,-1,1)


#escapeEvent = OnscreenText(
# 			 text="1: Set a Texture onto the Cube",
#     			 style=1, fg=(1,1,1,1), pos=(-1.3, 0.95),
#			 align=TextNode.ALeft, scale = .05)
#spaceEvent = OnscreenText(
# 			 text="2: Toggle Light from the front On/Off",
#     			 style=1, fg=(1,1,1,1), pos=(-1.3, 0.90),
#			 align=TextNode.ALeft, scale = .05)
#upDownEvent = OnscreenText(
# 			 text="3: Toggle Light from on top On/Off",
#     			 style=1, fg=(1,1,1,1), pos=(-1.3, 0.85),
#			 align=TextNode.ALeft, scale = .05)

#class MyTapper(DirectObject):
#	def __init__(self):
#		self.testTexture=loader.loadTexture("maps/envir-reeds.png")
#		self.accept("1", self.toggleTex)
#		self.accept("2", self.toggleLightsSide)
#		self.accept("3", self.toggleLightsUp)

#		self.LightsOn=False
#		self.LightsOn1=False
#		slight = Spotlight('slight')
#		slight.setColor(Vec4(1, 1, 1, 1))
#		lens = PerspectiveLens()
#		slight.setLens(lens)
#		self.slnp = render.attachNewNode(slight)
#		self.slnp1= render.attachNewNode(slight)

#	def toggleTex(self):
#		global cube
#		if cube.hasTexture():
#			cube.setTextureOff(1)
#		else:
#			cube.setTexture(self.testTexture)

#	def toggleLightsSide(self):
#		global cube
#		self.LightsOn=not(self.LightsOn)

#		if self.LightsOn:
#			render.setLight(self.slnp)
#			self.slnp.setPos(cube, 10,-400,0)
#			self.slnp.lookAt(Point3(10, 0, 0))
#		else:
#			render.setLightOff(self.slnp)

#	def toggleLightsUp(self):
#		global cube
#		self.LightsOn1=not(self.LightsOn1)

#		if self.LightsOn1:
#			render.setLight(self.slnp1)
#			self.slnp1.setPos(cube, 10,0,400)
#			self.slnp1.lookAt(Point3(10, 0, 0))
#		else:
#			render.setLightOff(self.slnp1)


#t=MyTapper()

run()

