from game import Game
from agent import Agent


class GameController:
    def __init__(self, game: Game, redPlayer: Agent, greenPlayer: Agent):
        self.redPlayerTurn = True
        self.game = game
        self.greenPlayer = greenPlayer
        self.redPlayer = redPlayer
        pass

    def play(self):
        # TODO: take choice from user to process the current turn or wait a certain amount of time
        currentPlayer = self.redPlayer if self.redPlayerTurn else self.greenPlayer
        bonusSoldiers = self.game.bonusSoldiers(self.redPlayerTurn)
        currentPlayer.applyHeuristic(self.game, bonusSoldiers)
        self.redPlayerTurn = not self.redPlayerTurn
