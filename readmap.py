import json

class Stage:
	def __init__(self, stageFile):
		file = open(stageFile)
		self.data = json.loads(file.read())
		file.close()
	
	def printRoom(self, roomId)
		#str = ""
		#for row in self.data:
		#	for tile in row:
		#		str += tile
		#	str += "\n"
		#print(str)


filename = "map.txt"
	

def readmap(filename):
	file = open(filename)
	map = []
	for line in file.readlines():
		map.append(list(c for c in line if c != '\n'))
	file.close()
	return map

data = readjson("stage.txt")
print data["stage-map"]
print data["start"]
for r in data["rooms"]:
	print r
#map = readmap(filename)
#output(map)
