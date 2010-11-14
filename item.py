import json
from model import *

def loadItens():
	file = open('cfg/itens.json')
	data = json.loads(file.read())
	file.close()
	return data

class Item(Model):

	ITENS = loadItens()

	def __init__(self,itemName):
		Model.__init__(self, Item.ITENS[itemName]['model'])
		self.name = itemName
		self.type = 'item'
		self.symbol = 'i'#Item.ITENS[self.name]['symbol']



