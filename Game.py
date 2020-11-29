import random
from constants import MIN_ARMY_START, MAX_ARMY_START


class Game:

    def __init__(self, map, isSimulation, redPlayer=None, greenPlayer=None):
        self.redPlayerTurn = True  # the red player starts first
        self.isSimulation = isSimulation
        self.map = map
        self.redPlayer = redPlayer
        self.greenPlayer = greenPlayer

    def prepare(self):
        for city in self.map.cityList:
            city.isRedArmy = True if random.randint(0, 1) == 0 else False
            city.armyCount = random.randint(MIN_ARMY_START, MAX_ARMY_START)  # random integer from 1 to 10 inclusive

    def play(self):
        # TODO: take choice from user to process the current turn
        if self.redPlayerTurn:
            self.redPlayer.applyHeuristic(self.map)
        else:
            self.greenPlayer.applyHeuristic(self.map)

    # debugging functions
    def __str__(self):
        return f'redPlayerTurn={self.redPlayerTurn}, isSimulation={self.isSimulation} \n{self.map.__str__()}'
