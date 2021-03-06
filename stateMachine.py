from direct.fsm.FSM import FSM
from direct.task import Task
from direct.showbase.ShowBase import ShowBase

from input import *
from character import *
from cam import *

from game import *
from newGame import *
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
			'Title':    ['NewGame','Options', 'Exit'],
			'NewGame':  ['InGame', 'Title'],
			'InGame':   ['Paused', 'GameOver'],
			'Paused':   ['InGame', 'Title', 'Exit'],
			'GameOver': ['Title', 'Exit'],
			'Options':  ['Title']
		}

		GameLoader.music = Music('Game')
		GameLoader.music.addTrack('no_entrance')
		GameLoader.music.addTrack('gameover')
		GameLoader.music.addSfx('key')

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

		waitTime = 0.016
		if self.states[self.state].waitTime > 0:
			waitTime = self.states[self.state].waitTime

		if task.time - self.lastTaskTime > waitTime: #0.016
			self.states[self.state].waitTime = 0

			newState = self.states[self.state].iterate()

			if newState:
				print(newState)
				self.request(newState)

			self.lastTaskTime = task.time
		return task.cont

	def enterTitle(self):
		GameLoader.music.setCurrent('no_entrance')
		GameLoader.music.play()
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
		self.states[self.newState] = NewGame()
		self.states[self.newState].register(self.render2d, self.cam, self.actionKeys)

	def enterInGame(self):
		# to do: read this from a config file
		# or from user interface
		if not self.states[self.newState]:
			initialStage = "stage/stage1.txt"
			chars = {'Jackson': Character("char/Jackson"),
					'Jackson2': Character("char/Jackson2")}

			self.states[self.newState] = Game(Stage(initialStage), chars, "Jackson", "Jackson2")
			self.states[self.newState].register(self.render, self.cam, self.actionKeys, self.render2d)
		else:
			self.states[self.newState].enter()

	def enterPaused(self):
		self.states[self.newState] = Pause()
		self.states[self.newState].register(self.render2d, self.cam, self.actionKeys)

	def enterGameOver(self):
		GameLoader.music.setCurrent('gameover')
		GameLoader.music.play()
		if not self.states[self.newState]:
			self.states[self.newState] = GameOver()
			self.states[self.newState].register(self.render2d, self.cam, self.actionKeys)
		else:
			self.states[self.newState].enter()

	def enterExit(self):
		exit()

	def exitInGame(self):
		self.states[self.oldState].exit()

	def exitNewGame(self):
		self.states[self.oldState].exit()

	def exitTitle(self):
		self.states[self.oldState].exit()

	def exitPaused(self):
		self.states[self.oldState].exit()

