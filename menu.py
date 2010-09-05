from direct.fsm.FSM import FSM
from direct.task import Task
from direct.showbase.ShowBase import ShowBase

from input import *
from game import *
from pause import *

# here goes the game logic:
# title menu state machine, etc

# http://www.panda3d.org/manual/index.php/Simple_FSM_Usage
class Menu(FSM, ShowBase, Input):
	def __init__(self, initialState='Title'):
		FSM.__init__(self, initialState)
		ShowBase.__init__(self)
		Input.__init__(self)

		self.defaultTransitions = {
			'Title':    ['NewGame', 'Options', 'Exit'],
			'NewGame':  ['InGame', 'Title'],
			'InGame':   ['Paused', 'GameOver'],
			'Paused':   ['InGame', 'Title', 'Exit'],
			'GameOver': ['Title', 'Exit'],
			'Options':  ['Title']
		}
		
		self.states = {}
		for state in self.defaultTransitions.keys():
			self.states[state] = None
		
		# Read KeyConfig from a json file
		kcfg = open("cfg/input.cfg")
		keyCfg = json.loads(kcfg.read())
		kcfg.close()
		
		self.inputMap(keyCfg)
		self.bindKeys()
		
		taskMgr.add(self.idle, "Idle")

		self.request(initialState)
	
	def idle(self, task):
		try:
			#print("I'm in '"+self.state)
			newState = self.states[self.state].iterate()
			if newState:
				self.request(newState)
		except:
			print("Error: State '"+ self.state +"' not registered...")
			
		return task.cont

	def enterTitle(self):
		pass
		
	def enterOptions(self):
		pass

	def enterNewGame(self):
		pass
		
	def enterInGame(self):
		# to do: read this from a config file
		if not self.states[self.newState]:
			initialStage = "stage/stage1.txt"
			self.states[self.newState] = Game(Stage(initialStage), [])
			self.states[self.newState].register(self.render, self.camera, self.actionKeys)
		
	def enterPaused(self):
		self.states[self.newState] = Pause()
		self.states[self.newState].register(self.render2d, self.camera, self.actionKeys)
		
	def enterGameOver(self):
		pass
		
	def enterExit(self):
		pass
		
	def exitPaused(self):
		self.states[self.oldState].exit()
