from Controllers.khan_controller import KhanGameController
from EngineConnectors.consol_display import consolDisplay
from EngineConnectors.pyxel_controller import PyxelDisplay


controller = KhanGameController()
display = PyxelDisplay(controller)
