import copy
import math
import random

from city import City
from map import Map


class Game:
    """"
    map: id of each city maps to ids of adjacent cities
    cityList: id of each city maps to information about this city
    soldiersCount:
                soldierCount[false]: number soldiers of green player
                soldierCount[true]: number soldiers of red player
                
    cityCount:
                cityCount[false]: number of cities that belong to green player
                cityCount[true]: number of cities that belong to red player
    """""

    def __init__(self, map: Map):
        self.map = map
        self.cityList = [City(i) for i in range(self.map.cityCount)]
        self.soldiersCount = {False: 0,
                              True: 0}
        self.cityCount = {False: 0,
                          True: 0}

    # this method need to be modified according to the pdf
    def prepare(self):
        # for city in self.cityList: -> di mlhash lzma
        # generate a list of false booleans with size 40
        for i in range(0, self.map.cityCount, 1):
            self.cityList[i].isRedArmy = False
            self.cityList[i].armyCount = 2
        # generate random 20 indices in range 0, 39
        res = random.sample(range(0, self.map.cityCount), 20)
        for i in range(0, len(res), 1):
            self.cityList[res[i]].isRedArmy = True
        self.initializeCounts()

    def getCityList(self):
        return self.cityList

    # to choose the number of army added to some city

    # conquer city with some army count
    def move(self, fromId: int, toId: int, soldiers: int):
        self.addSoldiersToCity(fromId, -soldiers)
        self.addSoldiersToCity(toId, -self.cityList[toId].armyCount)
        self.changeCityOwner(toId)
        self.addSoldiersToCity(toId, soldiers)

    def bonusSoldiers(self, isRedPlayer: bool):
        soldiersCount = self.soldiersCount[isRedPlayer]
        return max(math.floor(soldiersCount / 3), 3)

    def addSoldiersToCity(self, city_id: int, soldiers: int):
        self.cityList[city_id] += soldiers
        self.addSoldiersToPlayer(self.cityList[city_id].isRedArmy, soldiers)

    def addSoldiersToPlayer(self, isRedPlayer: bool, soldiers: int):
        self.soldiersCount[isRedPlayer] += soldiers

    def changeCityOwner(self, cityId: int):
        self.cityCount[self.cityList[cityId].isRedArmy] -= 1
        self.cityList[cityId].isRedArmy = not self.cityList[cityId].isRedArmy
        self.cityCount[self.cityList[cityId].isRedArmy] += 1

    def initializeCounts(self):
        for city in self.cityList:
            self.addSoldiersToCity(city.id, city.armyCount)

    # # debugging functions
    # def __str__(self):
    #     return f'redPlayerTurn={self.redPlayerTurn}, isSimulation={self.isSimulation} \n{self.map.__str__()}'
