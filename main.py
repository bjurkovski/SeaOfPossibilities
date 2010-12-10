#!/usr/bin/python

from game import *
from stateMachine import *

if __name__ == '__main__':
	#filename = "stage/map/1-1.txt"
	#m = Map(filename)
	#print m

	#filename = "stage/stage1.txt"
	#a = Stage(filename)
	#print a

	#game = Game(Stage("stage/stage1.txt"), [])
	#game.run()

	b = StateMachine('Title')
	b.run()

