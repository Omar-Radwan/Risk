from typing import List, Any
from Agent import Agent
from City import City
from Game import Game


class GreedyAgent(Agent):



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



    def applyHeuristic(self, game: Game, bonusPlayers: int):
        myMinArmyCityId = self.myMinArmyCity(game)
        u, v = self.hisMinArmyCityToAttack(game)
        game.addSoldiersTo(myMinArmyCityId, bonusPlayers)
        game.move(u, v, game.cityList[v].armyCount + 1)

# should add bonus players to city id
