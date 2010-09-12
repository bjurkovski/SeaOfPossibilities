import direct.directbase.DirectStart

from stage import *

stage = Stage('stage/stage1.txt')

render.attachNewNode(stage.maps["2"].getNode())

def idle(task):
	camera.setPos(0, -2, -2)
	camera.lookAt(0, 0, 0)

	return task.cont

taskMgr.add(idle,"id")

run()

