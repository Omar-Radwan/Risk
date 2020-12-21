import copy

from Agent import Agent
from Game import Game


class MiniMaxAgent(Agent):
    """
        isRedPlayer
        game
    """

    def __init__(self, isRedPlayer: bool, game: Game = None):
        super().__init__(isRedPlayer, game)
        self.stateFinder = StateFinder()

    def applyHeuristic(self, game, bonusPlayers):
        self.maximize(0, 3, game, int(-1e9), int(1e9))

    def evaluate(self, game: Game):
        result = 0
        for city in game.cityList:
            if (city.isRedArmy == self.isRedPlayer):
                result += 1
        return result

    def maximize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        if (self.shouldTerminate(curDepth, maxDepth, game)):
            return self.evaluate(game)
        bonusSoldiers = game.bonusSoldiers(self.isRedPlayer)
        states = self.stateFinder.adjacentStates1(game, bonusSoldiers, self.isRedPlayer)
        maxTuple = (None, int(-1e9))
        for game in states:
            copyGame = copy.deepcopy(game)
            curTuple = self.minimize(curDepth + 1, maxDepth, copyGame, alpha, beta)
            maxTuple = max(maxTuple, curTuple)
            alpha = max(alpha, maxTuple[1])
            if (alpha >= beta):
                break
        return maxTuple

    def minimize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        if (self.shouldTerminate(curDepth, maxDepth, game)):
            return self.evaluate(game)
        bonusSoldiers = game.bonusSoldiers(not self.isRedPlayer)
        states = self.stateFinder.adjacentStates1(game, bonusSoldiers, not self.isRedPlayer)
        minTuple = (None, int(1e9))
        for game in states:
            copyGame = copy.deepcopy(game)
            curTuple = self.maximize(curDepth + 1, maxDepth, copyGame, alpha, beta)
            minTuple = max(minTuple, curTuple)
            beta = min(beta, minTuple[1])
            if (alpha >= beta):
                break
        return minTuple

    def shouldTerminate(self, curDepth: int, maxDepth: int, game: Game) -> bool:
        if (curDepth == maxDepth):
            return True
        redCities = game.countSoldiers(True)
        if (redCities == 0 or redCities == game.map.cityCount):
            return True
        return False


class StateFinder:
    """
        assumptions:
            1. bonus soldiers are added to one city only
            2. attack city y from city x with y.armyCount+1 (with least number of soldiers able to conquer y)
    """""

    # O(cities^2 * adjacentCities)
    def adjacentStates1(self, game: Game, bonusSoldiers: int, isRedPlayer: bool) -> []:
        currentPlayerCitiesId = self.myCities(game, isRedPlayer)
        result = []
        for bonusArmyCityId in currentPlayerCitiesId:  # O(cities)
            copyGame1 = copy.deepcopy(game)
            copyGame1.addSoldiersTo(bonusArmyCityId, bonusSoldiers)
            for uId in currentPlayerCitiesId:  # O(cities)
                adjacentCitiesToU = game.map.graph[uId]
                for vId in adjacentCitiesToU:  # O(adjacent)
                    if (game.cityList[uId].isRedArmy != isRedPlayer
                            and game.cityList[uId].armyCount > game.cityList[vId].armyCount + 1):
                        copyGame2 = copy.deepcopy(copyGame1)
                        copyGame2.move(uId, vId, game.cityList[vId].armyCount + 1)
                        result.append(copyGame2)
        return result

    """
        assumptions:
            1. bonus soldiers are added to one city only
            2. attack city y from city x with [y.armyCount+1 ... x.armyCount-1]
    """

    # O(cities^2 * soldiers attacking * adjacentCities)
    def adjacentStates2(self, game: Game, bonusSoldiers: int, isRedPlayer: bool) -> []:
        currentPlayerCitiesId = self.myCities(game, isRedPlayer)
        result = []
        for bonusArmyCityId in currentPlayerCitiesId:  # O(cities)
            copyGame1 = copy.deepcopy(game)
            copyGame1.addSoldiersTo(bonusArmyCityId, bonusSoldiers)
            for uId in currentPlayerCitiesId:  # O(cities)
                adjacentCitiesToU = game.map.graph[uId]
                for vId in adjacentCitiesToU:  # O(adjacent)
                    if (game.cityList[uId].isRedArmy != isRedPlayer):
                        for soldiers in range(game.cityList[vId].armyCount + 1, game.cityList[uId],
                                              1):  # O(y.armyCount+1 ... x.armyCount-1)
                            copyGame2 = copy.deepcopy(copyGame1)
                            copyGame2.move(uId, vId, soldiers)
                            result.append(copyGame2)
        return result

    """
        find all cities that belong to a player 
    """

    def myCities(self, game: Game, isRedPlayer: bool) -> []:
        result = []
        for city in game.cityList:
            if (city.isRedArmy == isRedPlayer):
                result.append(city.id)
        return result

    """
    ideas:
        - create wrapper class called state that contains game and actions that led to that game 
    """""
