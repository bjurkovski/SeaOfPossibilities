import json

class Item():

	def __init__(self,filename):
		
		file = open(filename)
		self.data = json.loads(file.read())
		file.close()		
		

	def getModel(self,name):
		return self.data[name]['model']
		


