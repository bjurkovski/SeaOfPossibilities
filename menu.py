from direct.fsm.FSM import FSM
from game import *

# here goes the game logic:
# title menu state machine, etc

# http://www.panda3d.org/manual/index.php/Simple_FSM_Usage
class Menu(FSM):
	def __init__(self, initialState='Title'):
		FSM.__init__(self, 'Menu')

		self.defaultTransitions = {
			'Title': ['NewGame', 'MapEditor', 'Exit'],
			'NewGame': ['Title'],
			'MapEditor': ['Title']
		}

		self.request(initialState)

	def enterTitle(self):
		print("I'm currently on the Title state :)")

	def exitTitle(self):
		print("I'm quitting the Title state...")

	def enterNewGame(self):
		print("I'm currently on the NewGame state :)")
		# to do: read this from a config file
		initialStage = "stage/stage1.txt"
		game = Game(Stage(initialStage), [])
		game.run()

	def exitNewGame(self):
		pass
