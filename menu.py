from direct.fsm.FSM import FSM
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from game import *
from input import *

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
		
		# Read KeyConfig from a json file
		kcfg = open("cfg/input.cfg")
		keyCfg = json.loads(kcfg.read())
		self.inputMap(keyCfg)
		self.bindKeys()
		kcfg.close()
		
		taskMgr.add(self.idle, "Idle")

		self.request(initialState)
	
	def idle(self, task):
		try:
			self.states[self.state].iterate()
		except:
			print("Error: State not registered...")
			
		return task.cont

	def enterTitle(self):
		print("I'm currently on the Title state :)")

	def exitTitle(self):
		print("I'm quitting the Title state...")

	def enterNewGame(self):
		print("I'm currently on the NewGame state :)")
		# to do: read this from a config file
		initialStage = "stage/stage1.txt"
		self.states[self.newState] = Game(Stage(initialStage), [])
		self.states[self.newState].register(self.render, self.camera, self.actionKeys)

	def exitNewGame(self):
		pass
