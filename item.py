import json
from model import Model
 
class Item():

	def __init__(self,filename):
		
		file = open(filename)
		self.data = json.loads(file.read())
		file.close()		
		

	def getInstance(self, name):
		return {
			'name' : name,
			'instance' : Model(self.data[name]['model']),
			'symbol' : self.data[name]['symbol'],
			'type' : 'item'
		}




