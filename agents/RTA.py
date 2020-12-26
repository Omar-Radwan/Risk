from queue import PriorityQueue
from game import Game
from agent import Agent
import random
from copy import deepcopy

from heuristics import HeuristicsManager


class RealTime(Agent):

    # How many enemy cities can attack me in my new city if I decided to attack this new city.
    def dangerOnDefeatedCityHeuristic(self, enemyCity, newArmyInEnemyCity, danger, game: Game):
        for neighbourId in game.map.graph[enemyCity.id]:
            neighbour = game.cityList[neighbourId]
            if neighbour.isRedArmy == enemyCity.isRedArmy and neighbour.armyCount > newArmyInEnemyCity + 1:
                danger += 2
        return danger

    # How many enemies can attack me in my original city if I left it with only 1 army.
    def dangerOnOriginalCityHeuristic(self, myCity, newArmyInEnemyCity, danger, game: Game):
        for neighbourId in game.map.graph[myCity.id]:
            neighbour = game.cityList[neighbourId]
            if neighbour.isRedArmy != myCity.isRedArmy and neighbour.armyCount > newArmyInEnemyCity + 1:
                danger += 1
        return danger

    def calculateHeuristic(self, game: Game):
        # hnCost = 0
        # cityListId = game.citiesOf(self.isRedPlayer)
        # for cityId in cityListId:
        #     for neighbourId in game.map.graph[cityId]:
        #         city = game.cityList[cityId]
        #         neighbour = game.cityList[neighbourId]
        #         if neighbour.armyCount > city.armyCount + 1 and neighbour.isRedArmy != city.isRedArmy:
        #             hnCost += 1
        heuristicManager = HeuristicsManager()
        return game.cityCount[not self.isRedPlayer] + game.soldiersCount[not
        self.isRedPlayer] + heuristicManager.mySecuredCities(self.isRedPlayer, game)

        # put first node in pq

        # while !pq.empty
        # pop minimum
        # investigate adjacent nodes of minimum
        # continue

    def applyHeuristic(self, initialGame: Game):
        if (initialGame.isFinished()):
            return initialGame
        pq = PriorityQueue()
        # value,curGameState , game after first move in path
        visited = {}
        pq.put((0, 0, initialGame, initialGame))
        isFirstMove = True
        ansGame = None
        curTuple = (0, 0, initialGame, initialGame)
        while True:
            value, g, curGame, firstMoveInPath = minTuple = curTuple
            if (self.isGoalState(curGame, initialGame)):
                ansGame = firstMoveInPath
                break

        adjacentStates = self.adjacentStates(curGame)

        for nextGameState in adjacentStates:
            value: int
            newG = 0
            if (nextGameState in visited.keys()):
                value = visited[nextGameState][0]
                newG = visited[nextGameState][1]
            else:
                value = (newG + self.calculateHeuristic(nextGameState))
                newG = g + 1
            if (isFirstMove):
                pq.put((value, newG, nextGameState, nextGameState))
            else:
                pq.put((value, newG, nextGameState, firstMoveInPath))

        frontTuple = pq.get()
        visited[curTuple] = pq.get()
        curTuple = frontTuple
        isFirstMove = False
        return ansGame

    def isGoalState(self, gameState: Game, initialState: Game):
        return (gameState.cityCount[self.isRedPlayer] - initialState.cityCount[self.isRedPlayer] >= 2 or
                gameState.cityCount[self.isRedPlayer] == len(gameState.cityList))

    def adjacentStates(self, game: Game):
        bonusArmyPossibilities = list()
        cityListId = game.citiesOf(self.isRedPlayer)
        bonusArmy = game.bonusSoldiers(self.isRedPlayer)

        for cityId in cityListId:
            gameCopy = deepcopy(game)
            gameCopy.addSoldiersToCity(cityId, bonusArmy)
            bonusArmyPossibilities.append(gameCopy)

        attackingPossibilities = list()
        for gameStatee in bonusArmyPossibilities:
            cityListId = gameStatee.citiesOf(self.isRedPlayer)
            for cityId in cityListId:
                city = gameStatee.cityList[cityId]
                for neighbourId in gameStatee.map.graph[cityId]:
                    neighbour = gameStatee.cityList[neighbourId]
                    if city.armyCount > neighbour.armyCount + 1 and city.isRedArmy != neighbour.isRedArmy:
                        gameCopy = deepcopy(gameStatee)
                        gameCopy.move(cityId, neighbourId, neighbour.armyCount + 1)
                        attackingPossibilities.append(gameCopy)

        return attackingPossibilities

    def attack(self, fromCityId, toCityId, fromCityArmyCount, game):
        game.move(fromCityId, toCityId, fromCityArmyCount)
