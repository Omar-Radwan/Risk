from time import sleep

from agents.nearly_pacifist_agent import NearlyPacifistAgent
from game import Game
from game_engine import GameEngine
from gui import GUI
from map import Map


def start():
    gameState = GUI.GameState()
    map = Map()
    game = Game(map)
    gameEngine = GameEngine(True, game, NearlyPacifistAgent(True), NearlyPacifistAgent(False))
    while True:
        gameState.renderPlayingmode(gameEngine.game)
        sleep(0.05)
        gameEngine.play()


start()
