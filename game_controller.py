from game import Game
from agent import Agent
from copy import deepcopy


class GameController:
    def __init__(self, game: Game, redPlayer: Agent = None, greenPlayer: Agent = None):
        self.isRedPlayerTurn = True
        self.game = game
        self.players = {False: greenPlayer,
                        True: redPlayer}

    def play(self):
        # TODO: take choice from user to process the current turn or wait a certain amount of time
        self.players[self.isRedPlayerTurn].applyHeuristic(deepcopy(self.game))
        self.isRedPlayerTurn = not self.isRedPlayerTurn


