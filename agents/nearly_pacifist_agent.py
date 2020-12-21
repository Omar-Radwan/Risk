from typing import List, Any

from agent import Agent
from city import City
from game import Game


class NearlyPacifistAgent(Agent):

    def compareCity(self, x: City, y: City) -> bool:
        return x.armyCount < y.armyCount if x.armyCount != y.armyCount else x.id < y.id

    def myMinArmyCity(self, game: Game) -> int:
        myCities = game.citiesOf(self.isRedPlayer)
        minCity = myCities[0]
        for city in myCities:
            if (self.compareCity(city, minCity)):
                minCity = city
        return minCity.id

    def hisMinArmyCityToAttack(self, game: Game) -> ():
        myAdjToMin, hisMinCityId, graph = -1, -1, game.map.graph

        for u in self.cityList:
            uId = u.id
            for vId in graph[uId]:
                v = game.cityList[vId]
                if u.armyCount - 2 >= v.armyCount:
                    if hisMinCityId == -1:
                        myAdjToMin, hisMinCityId = uId, vId
                else:
                    current, candidate = game.cityList[hisMinCityId], game.cityList[vId]
                    if (self.compareCity(candidate, current)):
                        myAdjToMin, hisMinCityId = uId, vId
        return (myAdjToMin, hisMinCityId)

    def applyHeuristic(self, game: Game):
        myMinArmyCityId = self.myMinArmyCity(game)
        u, v = self.hisMinArmyCityToAttack(game)
        game.addSoldiersToPlayer(myMinArmyCityId)
        game.move(u, v, game.cityList[v].armyCount + 1)

# should add bonus players to city id
