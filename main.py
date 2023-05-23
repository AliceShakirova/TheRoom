from Controllers.khan_controller import KhanGameController
from EngineConnectors.consolDisplay import consolDisplay
from EngineConnectors.pyxelMode import PyxelDisplay


controller = KhanGameController()
controller.start_new_game(2)
display = PyxelDisplay(controller)
