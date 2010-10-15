from direct.fsm.FSM import FSM
from direct.task import Task
from direct.showbase.ShowBase import ShowBase

from input import *
from character import *
from cam import *

from game import *
from pause import *
from titleScreen import *
from options import *
from gameOver import *

# http://www.panda3d.org/manual/index.php/Simple_FSM_Usage
class StateMachine(FSM, ShowBase, Input):
	def __init__(self, initialState='Title'):
		FSM.__init__(self, initialState)
		ShowBase.__init__(self)
		Input.__init__(self)
		
		self.cam = Cam(self.camera)

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
			newState = self.states[self.state].iterate()
			if newState:
				self.request(newState)
		except KeyError:
			print("Error: State '"+ self.state +"' not registered...")
			
		return task.cont

	def enterTitle(self):
		if not self.states[self.newState]:
			self.states[self.newState] = TitleScreen()
			self.states[self.newState].register(self.render, self.cam, self.actionKeys)
		else:
			self.states[self.newState].enter()
		
	def enterOptions(self):
		if not self.states[self.newState]:
			self.states[self.newState] = Options()
			self.states[self.newState].register(self.render, self.cam, self.actionKeys)
		else:
			self.states[self.newState].enter()

	def enterNewGame(self):
		pass
		
	def enterInGame(self):
		# to do: read this from a config file
		# or from user interface
		if not self.states[self.newState]:
			initialStage = "stage/stage1.txt"
			chars = {'Jackson': Character("char/Jackson")}
			self.states[self.newState] = Game(Stage(initialStage), chars, "Jackson")
			self.states[self.newState].register(self.render, self.cam, self.actionKeys)
		else:
			self.states[self.newState].enter()
		
	def enterPaused(self):
		self.states[self.newState] = Pause()
		self.states[self.newState].register(self.render2d, self.cam, self.actionKeys)
		
	def enterGameOver(self):
		if not self.states[self.newState]:
			self.states[self.newState] = GameOver()
			self.states[self.newState].register(self.render, self.cam, self.actionKeys)
		else:
			self.states[self.newState].enter()
		
	def enterExit(self):
		exit()
		
	def exitPaused(self):
		self.states[self.oldState].exit()