from character import *

class Player:
	id = 0 # <- FIX ME!
	def __init__ (self, character, id = -1) :
		if id == -1:
			self.id = Player.id
			Player.id += 1
		else :
			self.id = id
		
		self.character = character
	
	def __eq__ (self, other) :
		return self.id == other.id
	
	def sendCommand(self) :
		#self.character.tryToMove = []
		self.character.tryToDo = None


class HumanPlayer(Player):
	def __init__ (self, character, keys, id = -1) :
		Player.__init__(self, character, id)
		self.keys = keys
	
	def sendCommand(self) : 
		Player.sendCommand(self)
		
		#directions = [key for key in ["up%d"%(self.id),"down%d"%(self.id),"left%d"%(self.id),"right%d"%(self.id)] if self.keys[key]]
		#directions = [key for key in ["up","down","left","right"] if self.keys[key]]
		directions = [key for key in ["up","down","left","right"] if self.keys[key] or self.keys[key+"%d"%(self.id)]]
		self.character.tryToMove = directions
		
		#actions = [key for key in ["action%d"%(self.id),"attack%d"%(self.id),"cancel%d"%(self.id)] if self.keys[key]]
		actions = [key for key in ["action","attack","cancel"] if self.keys[key]]
		if len(actions) != 0 :
			self.character.tryToDo = actions[0] #Soh deve executar uma action!
		
