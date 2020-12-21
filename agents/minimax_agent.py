from action_manager import ActionManager
from agent import Agent
from game import Game


class MiniMaxAgent(Agent):

    def __init__(self, isRedPlayer: bool, game: Game = None):
        super().__init__(isRedPlayer)
        self.actionManager = ActionManager(game)

    def applyHeuristic(self, game: Game):
        value, bonusArmyAction, attackAction = self.maximize(0, 3, game, int(-1e9), int(1e9))
        if bonusArmyAction != None:
            bonusArmyAction.apply()
        if attackAction != None:
            attackAction.apply()

    def maximize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        if (self.terminalState(curDepth, maxDepth, game)):
            return (self.evaluate(game), None, None)

        actionTuples = self.actionManager.adjacentActions1(self.isRedPlayer)  #
        maxTuple = (int(-1e9), None, None)  #

        for actionTuple in actionTuples:

            bonusSoldiersAction, attackActionList = actionTuple[0], actionTuple[1]
            bonusSoldiersAction.apply()

            for attackAction in attackActionList:

                attackAction.apply()
                childTuple = self.minimize(curDepth + 1, maxDepth, game, alpha, beta)  #
                self.actionManager.rollBackAction()

                if childTuple[0] > maxTuple[0]:  #
                    maxTuple = (childTuple[0], bonusSoldiersAction, attackAction)  #

                alpha = max(alpha, maxTuple[0])  #

                if (alpha >= beta):
                    break

            self.actionManager.rollBackAction()

        return maxTuple  #

    def minimize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        if (self.terminalState(curDepth, maxDepth, game)):
            return (self.evaluate(game), None, None)

        actionTuples = self.actionManager.adjacentActions1(not self.isRedPlayer)  #
        minTuple = (int(1e9), None, None)  #

        for actionTuple in actionTuples:

            bonusSoldiersAction, attackActionList = actionTuple[0], actionTuple[1]
            bonusSoldiersAction.apply()

            for attackAction in attackActionList:

                attackAction.apply()
                childTuple = self.maximize(curDepth + 1, maxDepth, game, alpha, beta)  #
                self.actionManager.rollBackAction()

                if childTuple[0] < minTuple[0]:  #
                    minTuple = (childTuple[0], bonusSoldiersAction, attackAction)  #

                beta = min(beta, minTuple[0])  #

                if (alpha >= beta):
                    break

            self.actionManager.rollBackAction()

        return minTuple  #

    def terminalState(self, curDepth: int, maxDepth: int, game: Game) -> bool:
        if (curDepth == maxDepth or game.cityCount[self.isRedPlayer] == 0 or
                game.cityCount[self.isRedPlayer] == game.map.cityCount):
            return True
        return False

    def evaluate(self, game: Game):
        return game.cityCount[self.isRedPlayer] * 2 + game.soldiersCount[self.isRedPlayer]

# code that copies game a lot
# class StateFinder:
#     """
#         assumptions:
#             1. bonus soldiers are added to one city only
#             2. attack city y from city x with y.armyCount+1 (with least number of soldiers able to conquer y)
#     """""
#
#     # O(cities^2 * adjacentCities)
#     def adjacentStates1(self, game: Game, bonusSoldiers: int, isRedPlayer: bool) -> []:
#         currentPlayerCitiesId = self.myCities(game, isRedPlayer)
#         result = []
#         for bonusArmyCityId in currentPlayerCitiesId:  # O(cities)
#             copyGame1 = copy.deepcopy(game)
#             copyGame1.addSoldiersToPlayer(bonusArmyCityId, bonusSoldiers)
#             for uId in currentPlayerCitiesId:  # O(cities)
#                 adjacentCitiesToU = game.map.graph[uId]
#                 for vId in adjacentCitiesToU:  # O(adjacent)
#                     if (game.cityList[uId].isRedArmy != isRedPlayer
#                             and game.cityList[uId].armyCount > game.cityList[vId].armyCount + 1):
#                         copyGame2 = copy.deepcopy(copyGame1)
#                         copyGame2.move(uId, vId, game.cityList[vId].armyCount + 1)
#                         result.append(copyGame2)
#         return result
#
#     """
#         assumptions:
#             1. bonus soldiers are added to one city only
#             2. attack city y from city x with [y.armyCount+1 ... x.armyCount-1]
#     """
#
#     # O(cities^2 * soldiers attacking * adjacentCities)
#     def adjacentStates2(self, game: Game, bonusSoldiers: int, isRedPlayer: bool) -> []:
#         currentPlayerCitiesId = self.myCities(game, isRedPlayer)
#         result = []
#         for bonusArmyCityId in currentPlayerCitiesId:  # O(cities)
#             copyGame1 = copy.deepcopy(game)
#             copyGame1.addSoldiersToPlayer(bonusArmyCityId, bonusSoldiers)
#             for uId in currentPlayerCitiesId:  # O(cities)
#                 adjacentCitiesToU = game.map.graph[uId]
#                 for vId in adjacentCitiesToU:  # O(adjacent)
#                     if (game.cityList[uId].isRedArmy != isRedPlayer):
#                         for soldiers in range(game.cityList[vId].armyCount + 1, game.cityList[uId],
#                                               1):  # O(y.armyCount+1 ... x.armyCount-1)
#                             copyGame2 = copy.deepcopy(copyGame1)
#                             copyGame2.move(uId, vId, soldiers)
#                             result.append(copyGame2)
#         return result
#
#     """
#         find all cities that belong to a player
#     """
#
#     def myCities(self, game: Game, isRedPlayer: bool) -> []:
#         result = []
#         for city in game.cityList:
#             if (city.isRedArmy == isRedPlayer):
#                 result.append(city.id)
#         return result
