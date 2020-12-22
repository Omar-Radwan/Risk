import copy
import math
import random

from city import City
from map import Map


class Game:
    """
    Attributes:
        map: id of each city maps to ids of adjacent cities
        cityList: id of each city maps to information about this city
        soldiersCount:
                    soldierCount[false]: number soldiers of green player
                    soldierCount[true]: number soldiers of red player

        cityCount:
                    cityCount[false]: number of cities that belong to green player
                    cityCount[true]: number of cities that belong to red player
    """

    def __init__(self, map: Map, gameimage):
        self.map = map
        self.gameimage = gameimage
        if gameimage == "US":
            self.cityList = [City(i) for i in range(self.map.USmap.cityCount)]
        else:
            self.cityList = [City(i) for i in range(self.map.worldmap.cityCount)]
        self.soldiersCount = {False: 0,
                              True: 0}
        self.cityCount = {False: 0,
                          True: 0}

    # this method need to be modified according to the pdf
    def prepare(self):
        """
            prepares the game in the beginning
        :return:
        """
        # for city in self.cityList: -> di mlhash lzma
        # generate a list of false booleans with size 40
        for i in range(0, self.map.cityCount, 1):
            self.cityList[i].isRedArmy = False
            self.cityList[i].armyCount = 1
        # generate random 20 indices in range 0, 39
        res = random.sample(range(0, self.map.cityCount), 20)
        for i in range(0, len(res), 1):
            self.cityList[res[i]].isRedArmy = True
        self.initializeCounts()

    def getCityList(self):
        return self.cityList

    def move(self, fromId: int, toId: int, soldiers: int):
        """
        attacks city from adjacent one with some number of soldiers
        the two cities must have different type of soldiers
        the number of soldiers in the city to be attacked must be less than number of attacking soldiers
        :param fromId: id of the city which the attack is from
        :param toId: id of the city to be attacked
        :param soldiers: number of soldiers attacking
        :return:
        """
        print(f'fromId={fromId}, toId={toId}, soldiers={soldiers}')
        self.addSoldiersToCity(fromId, -soldiers)
        self.addSoldiersToCity(toId, -self.cityList[toId].armyCount)
        self.changeCityOwner(toId)
        self.addSoldiersToCity(toId, soldiers)

    def bonusSoldiers(self, isRedPlayer: bool):
        """
        calculates the number of bonus soldiers some player should receive according to current game state
        :param isRedPlayer: type of the player
        :return:
        """
        soldiersCount = self.soldiersCount[isRedPlayer]
        return max(math.floor(soldiersCount / 3), 3)

    def addSoldiersToCity(self, city_id: int, soldiers: int):
        """
        add certain number of soldiers to some city
        :param city_id: id of the city to which soldiers will be added
        :param soldiers: number of soldiers to be added
        :return:
        """
        self.cityList[city_id].armyCount += soldiers
        self.soldiersCount[self.cityList[city_id].isRedArmy] += soldiers

    def changeCityOwner(self, cityId: int):
        """
        changes the owner of some city after it's conquered
        :param cityId: id of conquered city
        :return:
        """
        self.cityCount[self.cityList[cityId].isRedArmy] -= 1
        self.cityList[cityId].isRedArmy = not self.cityList[cityId].isRedArmy
        self.cityCount[self.cityList[cityId].isRedArmy] += 1

    def initializeCounts(self):
        """
        uses cityList to initialize soldiersCount and cityCount
        :return:
        """
        for city in self.cityList:
            self.soldiersCount[city.isRedArmy] += city.armyCount
            self.cityCount[city.isRedArmy] += 1

    def citiesOf(self, isRedPlayer: bool) -> [int]:
        """
        :param isRedPlayer: type of the player
        :return: list of int containing ids of cities that belong to the selected player
        """
        result = []
        for city in self.cityList:
            if city.isRedArmy == isRedPlayer:
                result.append(city.id)
        return result

# # debugging functions
# def __str__(self):
#     return f'redPlayerTurn={self.redPlayerTurn}, isSimulation={self.isSimulation} \n{self.map.__str__()}'
