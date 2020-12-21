from typing import List

from city import City
from game import Game
from map import Map


class Agent:
    """

    """

    def __init__(self, isRedPlayer: bool):
        self.isRedPlayer = isRedPlayer

    def applyHeuristic(self, game: Game):
        pass

    # def attachCity(self, city: City):
    #     self.cityList.append(city)

    # # TODO: double check that this function is working correctly
    # def removeCity(self, city: City):
    #     self.cityList.remove(city)

    # lazm tt3dl 3shan cityList w game etshalo
    # bonusArmy is added to certain cities such that it maximizes my number of safe cities where
    # enemies can't attack it.
    def bonusArmyHeuristic(self, map: Map, bonusArmy):
        tupleList = []
        maximumArmyNeededToBeSafe = 0
        # loop on each city owned by the agent and get maximum number
        # of armies needed to be added in this city to be safe and
        # store them in tuple <city,maximumArmyNeededToBeSafe> and store each tuple in tupleList
        for city in self.cityList:
            for neighborId in map.graph[city.id]:
                neighbor = self.game.cityList[neighborId]
                if neighbor.isRedArmy != city.isRedArmy and neighbor.armyCount > city.armyCount + 1:
                    neededArmyToBeSafe = neighbor.armyCount - city.armyCount - 1
                    maximumArmyNeededToBeSafe = max(maximumArmyNeededToBeSafe, neededArmyToBeSafe)

            newTuple = (city, maximumArmyNeededToBeSafe)
            tupleObject = tuple(newTuple)
            tupleList.append(tupleObject)
        tupleList.sort(key=lambda x: x[1])
        # loop on tupleList which is sorted in ascending order according to maximumArmyNeededToBeSafe
        # and add maximumArmyNeededToBeSafe to the city to make it safe (if can)
        for singleTuple in tupleList:
            cityToBeSafe = singleTuple.__getitem__(0)
            maximumArmyToBeSafe = singleTuple.__getitem__(1)

            if maximumArmyToBeSafe <= bonusArmy:
                bonusArmy -= maximumArmyToBeSafe
                cityToBeSafe.armyCount += maximumArmyToBeSafe

            elif neededArmyToBeSafe > bonusArmy:
                cityToBeSafe.armyCount += bonusArmy
                bonusArmy = 0

            if bonusArmy == 0:
                break

    # # TODO: get rid of loop in this function
    # def countArmy(self) -> int:
    #     sum = 0
    #     for city in self.cityList:
    #         sum += city.armyCount
    #     return sum

    # # debugging function
    # def __str__(self):
    #     s = ""
    #     for city in self.cityList:
    #         s += city.__str__() + '\n'
    #     return s
    #
    # def myCities(self, isRedPlayer: bool) -> []:
    #     result = []
    #     for city in self.game.cityList:
    #         if (city.isRedArmy == isRedPlayer):
    #             result.append(city.id)
    #     return result
