
from queue import PriorityQueue
from game import Game
from agent import Agent
import random
from copy import deepcopy
class AStarAgent(Agent):


    #How many enemy cities can attack me in my new city if I decided to attack this new city.
    def dangerOnDefeatedCityHeuristic(self, enemyCity, newArmyInEnemyCity, danger,game:Game):
            for neighbourId in game.map.graph[enemyCity.id]:
                neighbour=game.cityList[neighbourId]
                if neighbour.isRedArmy==enemyCity.isRedArmy and neighbour.armyCount>newArmyInEnemyCity+1:
                    danger+=2
            return danger

    #How many enemies can attack me in my original city if I left it with only 1 army.
    def dangerOnOriginalCityHeuristic(self, myCity, newArmyInEnemyCity, danger,game:Game):
            for neighbourId in game.map.graph[myCity.id]:
                neighbour=game.cityList[neighbourId]
                if neighbour.isRedArmy!=myCity.isRedArmy and neighbour.armyCount>newArmyInEnemyCity+1:
                    danger+=1
            return danger


    def calculateHeuristic(self,game:Game):
        hnCost=0
        cityListId=game.citiesOf(self.isRedPlayer)
        for cityId in cityListId:
            for neighbourId in game.map.graph[cityId]:
                city =game.cityList[cityId]
                neighbour=game.cityList[neighbourId]
                if neighbour.armyCount>city.armyCount+1 and neighbour.isRedArmy!=city.isRedArmy:
                    hnCost+=1



    def applyHeuristic(self,game:Game):
        q = PriorityQueue()
        bonusSoldiers=game.bonusSoldiers(self.isRedPlayer)
        gnCost=0
        children=self.getChildren(bonusSoldiers,game)
        for childGameState in children:
            hnCost=self.calculateHeuristic(childGameState['child'])
            q.put(hnCost+gnCost,childGameState['child'],childGameState)

        while not q.empty():



        return game

    def getChildren(self,bonusArmy,game:Game):
        bonusArmyPossibilities=list()
        cityListId=game.citiesOf(self.isRedPlayer)

        for cityId in cityListId:
            gameCopy=deepcopy(game)
            gameCopy.addSoldiersToCity(cityId,bonusArmy)
            bonusArmyPossibilities.append(gameCopy)

        attackingPossibilities=list()
        for gameStatee in bonusArmyPossibilities:
            cityListId = gameStatee.citiesOf(self.isRedPlayer)
            for cityId in cityListId:
                for neighbourId in gameStatee.map.graph[cityId]:
                    neighbour = gameStatee.cityList[neighbourId]
                    city = gameStatee.cityList[cityId]
                    if city.armyCount > neighbour.armyCount + 1 and city.isRedArmy != neighbour.isRedArmy:
                        gameCopy=deepcopy(gameStatee)
                        gameCopy.move(cityId,neighbourId,city.armyCount-1)
                        attackingPossibilities.append({
                            'parent': gameStatee,
                            'child':gameCopy
                        })

        return attackingPossibilities



    def attack(self,fromCityId,toCityId,fromCityArmyCount,game):
        game.move(fromCityId,toCityId,fromCityArmyCount)