# send game state and return the new game state
# togggle the redArmy boolean in each agent or state
# check if the parameters are sent by reference not by value
import math

from agent import Agent
from city import City
from game import Game


class AggressiveAgent(Agent):
    def calculateMaxCity(self, list, game):
        max = 0
        if len(list) != 0:
            maxCity = game.cityList[list[0]]
        else:
            return
        for cityId in list:
            city = game.cityList[cityId]
            if (city.armyCount > max):
                max = city.armyCount
                maxCity = city

        return maxCity

    def applyHeuristic(self, game: Game) -> Game:
        cityListId = game.citiesOf(self.isRedPlayer)
        bonusArmy = game.bonusSoldiers(self.isRedPlayer)
        maxCity = self.calculateMaxCity(cityListId, game)
        if maxCity != None:
            game.addSoldiersToCity(maxCity.id, bonusArmy)
        # attack all neighbour cities with most armies
        for cityId in cityListId:
            for neighbourId in game.map.graph[cityId]:
                neighbour = game.cityList[neighbourId]
                city = game.cityList[cityId]
                if neighbour.armyCount < city.armyCount - 1 and neighbour.isRedArmy != city.isRedArmy:
                    game.move(city.id, neighbour.id, city.armyCount - 1)
        return game
