from time import sleep

from agents.minimax_agent import MiniMaxAgent
from agents.nearly_pacifist_agent import NearlyPacifistAgent
from game_engine import GameEngine
from game_engine import GameEngine
from game import Game
from gui import GUI
from map import Map


class LogicGuiController:
    def __init__(self):
        pass

    def start(self):
        # gui = GUI()
        # isSimulation, redAgentString, greenAgentString = gui.introScenes()
        gameState = GUI.GameState()
        map = Map()
        game = Game(map)
        gameEngine = GameEngine(True, game, NearlyPacifistAgent(True), NearlyPacifistAgent(False))
        while True:
            gameState.renderPlayingmode(gameEngine.game)
            sleep(3)
            gameEngine.play()
        pass

    def setTuple(self, isSimulation, aiAgent, nonAiAgent):
        gameState = GUI.GameState()
        print(gameState.intro())
        # tul ma m7dsh ksab el while tsht8l w ana sh8ala 3al simulation bs dlw2ty

        # print(isSimulation)
        # print(aiAgent)
        # print(nonAiAgent)

        # start the gui and take choices from the user
        # tuple(isSimulation, agent1, agent2)
        # create gameEngine and attach game to it
        # render the initial state of the game
        # ask gameEngine to process a play
        # render the new game to gui
        # ask gameEngine to process a new play
        # ........
