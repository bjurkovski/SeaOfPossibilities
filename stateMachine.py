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

		self.lastTaskTime = 0

		self.cam = Cam(self.cam)

		self.defaultTransitions = {
			# this changed, must go back to normal
			'Title':    ['NewGame','InGame', 'Options', 'Exit'],
			'NewGame':  ['InGame', 'Title'],
			'InGame':   ['Paused', 'GameOver'],
			'Paused':   ['InGame', 'Title', 'Exit'],
			'GameOver': ['Title', 'Exit'],
			'Options':  ['Title']
		}

		self.music = Music('game')
		self.music.addTrack('opening')

		#enable shaders in every model
		self.render.setShaderAuto()

		#disables mouse controlled camera
		self.disableMouse()

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
#		try:
		if task.time - self.lastTaskTime > 0.016: #0.016
			newState = self.states[self.state].iterate()
			if newState:
				print(newState)
				self.request(newState)

			self.lastTaskTime = task.time
#		except KeyError as e:
#			print("Error: State '"+ self.state +"' not registered...")
#			print(e)
		return task.cont

	def enterTitle(self):
		#TODO integrate music with the loader
		self.music.setCurrent('opening')
		self.music.play()
		if not self.states[self.newState]:
			self.states[self.newState] = TitleScreen()
			self.states[self.newState].register(self.render2d, self.cam, self.actionKeys)
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
			initialStage = "stage/stage1.txt", "stage/stage1-map.txt"
			chars = {'Jackson': Character("char/Jackson"),
					'Jackson2': Character("char/Jackson2")}

			self.states[self.newState] = Game(Stage(*initialStage), chars, "Jackson", "Jackson2")
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

	def exitTitle(self):
		self.states[self.oldState].exit()

	def exitPaused(self):
		self.states[self.oldState].exit()

