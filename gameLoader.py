import json
from panda3d.core import NodePath, CardMaker

from panda3d.core import CollisionNode, CollisionHandler, CollisionSphere, CollisionRay, CollisionHandlerPusher, CollisionTraverser, CollisionHandlerEvent, CollisionPolygon
from panda3d.core import Point3

def arrayToDict(a):
	h = {}
	for i in a:
		h[i[0]] = i[1]
		
	return h

class GameLoader():
	
	def __init__(self):
		self.data = {}
		self.cardMaker = CardMaker("card")
		self.data["textures"] = {}
	
	def loadFile(self,filename):
		try:
			file = open("stages/" + filename)
			data = json.loads(file.read())
			self.data["name"] = data["name"]
			self.data["start"] = data["start"]
			
			[ self.loadTexture(x) for x in data["textures"] ]
			 
			self.data["screens"] = arrayToDict ( [ [x.split(".")[0],self.loadScreen(x)] for x in data["screens"] ] )
			
			self.data["lanes"] = self.lanesLoader.loadFile(data["lanes"])
			
			self.data["music"] = Music(self.data["name"])
			for track in data["music"]:
				self.data["music"].addTrack(track)
			self.data["music"].setCurrent = data["music"][0]

			#self.data["models"] = 
		except Exception as e:
			print "Error opening: %s . %s" % (filename,e)

	def loadDefaults(self):
		self.cardMaker = CardMaker("card")
		self.textures = {}
		self.menu = self.makeMenu()

	def loadTexture(self,name):
		if name in self.data["textures"]:
			print("You already loaded the texture %s" % (name) )

		self.data["textures"][name] = loader.loadTexture("tex/%s" % (name) )
		
		return self.data["textures"][name]
	
	def loadScreen(self,tex):
		self.data["textures"][tex] = self.loadTexture(tex)
		self.cardMaker.setFrame(-1,1,-1,1)
		node = NodePath(self.cardMaker.generate())
		node.setTexture(self.data["textures"][tex])
		return node
		
	#to access data members inside the data hash
	def __getitem__(self, m):
		return self.data.get(m, None)


