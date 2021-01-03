from queue import PriorityQueue
from game_componenets.game import Game
from agents.agent import Agent
from copy import deepcopy

from game_componenets.heuristics import HeuristicsManager


class RealTime(Agent):

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
        self.isRedPlayer] + heuristicManager.mySecuredCities(not self.isRedPlayer, game)

        # put first node in pq

        # while !pq.empty
        # pop minimum
        # investigate adjacent nodes of minimum
        # continue

    def applyHeuristic(self, initialGame: Game):
        if (initialGame.isFinished()):
            return initialGame
        pq = PriorityQueue()
        visited = {}
        isFirstMove = True
        #           value, g, currentState, firstMoveThatLedToThisState, parent
        curTuple = (0, initialGame, initialGame, None)

        while True:
            value, curGame, firstMoveInPath, parent = curTuple
            if (self.isGoalState(curGame, initialGame)):
                ansGame = firstMoveInPath
                break
            adjacentStates = self.adjacentStates(curGame)
            if (parent != None):
                adjacentStates.append(parent)
            for nextGameState in adjacentStates:
                value: int
                newG: int
                if (nextGameState in visited.keys()):
                    value = visited[nextGameState][0] + 1

                else:
                    newG = 1
                    value = (newG + self.calculateHeuristic(nextGameState))
                if (isFirstMove):
                    pq.put((value, nextGameState, nextGameState, curGame))
                else:
                    pq.put((value, nextGameState, firstMoveInPath, curGame))

            frontTuple = pq.get()
            curState = frontTuple[1]
            visited[curState] = pq.get()
            curTuple = frontTuple
            isFirstMove = False
        return ansGame

    def isGoalState(self, gameState: Game, initialState: Game):
        return (gameState.cityCount[self.isRedPlayer] - initialState.cityCount[self.isRedPlayer] >= 5 or
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
