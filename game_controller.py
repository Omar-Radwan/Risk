from game import Game
from agent import Agent
from copy import deepcopy
# from gui import GUI

class GameEngine:
    def __init__(self,isSimulation, game: Game, redPlayer: Agent = None, greenPlayer: Agent = None):
        self.isRedPlayerTurn = True
        self.game = game
        self.players = {False: greenPlayer,
                        True: redPlayer}
        self.isSimulationMode=isSimulation
        self.isPlayingMode=not isSimulation
        game.prepare()

    def play(self):
        # TODO: take choice from user to process the current turn or wait a certain amount of time
        game=self.players[self.isRedPlayerTurn].applyHeuristic(deepcopy(self.game))
        self.isRedPlayerTurn = not self.isRedPlayerTurn






