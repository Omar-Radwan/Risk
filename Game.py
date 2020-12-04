import copy
import math
import random
from Agent import Agent
from City import City
from Map import Map
from constants import MIN_ARMY_START, MAX_ARMY_START


class Game:

    def __init__(self, map: Map, isSimulation: bool, redPlayer:Agent =None, greenPlayer:Agent =None):
        self.redPlayerTurn = True  # the red player starts first
        self.isSimulation = isSimulation
        self.map = map
        self.cityList = [City(i) for i in range(self.map.cityCount + 1)]
        self.redPlayer = redPlayer
        self.greenPlayer = greenPlayer


    # this method need to be modified according to the pdf
    def prepare(self):
        for city in self.cityList:
            city.isRedArmy = bool(random.getrandbits(1))
            city.armyCount = random.randint(MIN_ARMY_START, MAX_ARMY_START)  # random integer from 1 to 10 inclusive
            self.redPlayer.attachCity(city) if city.isRedArmy else self.greenPlayer.attachCity(city)

    def play(self):
        # TODO: take choice from user to process the current turn or wait a certain amount of time
        currentPlayer = self.redPlayer if self.redPlayerTurn else self.greenPlayer
        bonusPlayers = max(math.floor(len(currentPlayer.cityList) / 3), 3)

    # to choose the number of army added to some city
    def addSoldiersTo(self, city_id, soldiersCount):
        self.cityList[city_id] += soldiersCount

    # conquer city with some army count
    def move(self, from_id, to_id, count: int):
        self.cityList[from_id].armyCount-=count
        self.cityList[to_id].armyCount=count
        self.cityList[to_id].isRedArmy=self.cityList[from_id].isRedArmy
        if self.cityList[from_id].isRedArmy:
            self.redPlayer.attachCity(self.cityList[to_id])
        else :
            self.greenPlayer.attachCity(self.cityList[to_id])

    # debugging functions
    def __str__(self):
        return f'redPlayerTurn={self.redPlayerTurn}, isSimulation={self.isSimulation} \n{self.map.__str__()}'
