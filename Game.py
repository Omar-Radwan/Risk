import math
import random
from constants import MIN_ARMY_START, MAX_ARMY_START

class Game:

    def __init__(self, map, isSimulation, redPlayer=None, greenPlayer=None):
        self.redPlayerTurn = True  # the red player starts first
        self.isSimulation = isSimulation
        self.map = map
        self.redPlayer = redPlayer
        self.greenPlayer = greenPlayer

    # this method need to be modified according to the pdf
    def prepare(self):
        for city in self.map.cityList:
            city.isRedArmy = bool(random.getrandbits(1))
            city.armyCount = random.randint(MIN_ARMY_START, MAX_ARMY_START)  # random integer from 1 to 10 inclusive
            self.redPlayer.attachCity(city) if city.isRedArmy else self.greenPlayer.attachCity(city)

    def play(self):
        # TODO: take choice from user to process the current turn or wait a certain amount of time
        currentPlayer = self.redPlayer if self.redPlayerTurn else self.greenPlayer
        bonusPlayers = max(math.floor(len(currentPlayer.cityList) / 3), 3)

    # debugging functions
    def __str__(self):
        return f'redPlayerTurn={self.redPlayerTurn}, isSimulation={self.isSimulation} \n{self.map.__str__()}'
