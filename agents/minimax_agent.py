from random import random

from action_manager import ActionManager, BonusSoldiersAction, AttackAction
from agent import Agent
from game import Game
from heuristics import HeuristicsManager


class MiniMaxAgent(Agent):

    def __init__(self, isRedPlayer: bool):
        super().__init__(isRedPlayer)
        self.heuristicManager = HeuristicsManager()
        self.cnt = 0

    def applyHeuristic(self, game: Game) -> Game:
        """
        apply best bonus army action and best attack action specified by minimax algorithm
        :param game:
        :return: game instance after applying best actions specified by minimax algorithm
        """
        self.actionManager = ActionManager(game)

        self.cnt = 0
        value, bonusArmyActionList, attackAction = self.maximize(0, 1, game, int(-1e18), int(1e18))
        print("TerminalStates= ", self.cnt)
        if bonusArmyActionList != None:
            self.actionManager.applyListOfActions(bonusArmyActionList)
        if attackAction != None:
            self.actionManager.applyAction(attackAction)
        return game

    def maximize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        """
        :param curDepth: current state depth
        :param maxDepth: maximum allowed state depth
        :param game:
        :param alpha: maximum state value
        :param beta: minimum state value
        :return: tuple containing:  value of maximum state, best bonus army action, best attack action
        """
        if (self.terminalState(curDepth, maxDepth, game)):
            return (self.evaluate2(game), None, None)

        actionTuples = self.actionManager.adjacentActions2(self.isRedPlayer)
        maxTuple = (int(-1e18), actionTuples[0][0], None)  #
        broke = False

        for actionTuple in actionTuples:

            bonusSoldiersActionList, attackActionList = actionTuple[0], actionTuple[1]

            self.actionManager.applyListOfActions(bonusSoldiersActionList)

            for attackAction in attackActionList:
                self.actionManager.applyAction(attackAction)
                childTuple = self.minimize(curDepth + 1, maxDepth, game, alpha, beta)  #
                self.actionManager.rollBackAction()
                if (childTuple[0], random()) > (maxTuple[0], random()):  #
                    maxTuple = (childTuple[0], bonusSoldiersActionList, attackAction)  #

                alpha = max(alpha, maxTuple[0])  #
                if alpha >= beta:
                    broke = True
                    break

            self.actionManager.rollBackNAction(len(bonusSoldiersActionList))

            if broke:
                return maxTuple
        return maxTuple  #

    def minimize(self, curDepth: int, maxDepth: int, game: Game, alpha: int, beta: int):
        """
        :param curDepth: current state depth
        :param maxDepth: maximum allowed state depth
        :param game:
        :param alpha: maximum state value
        :param beta: minimum state value
        :return: tuple containing:  value of maximum state, best bonus army action, best attack action
        """
        if (self.terminalState(curDepth, maxDepth, game)):
            return (self.evaluate2(game), None, None)

        actionTuples = self.actionManager.adjacentActions2(not self.isRedPlayer)
        minTuple = (int(1e18), None, None)  #
        broke = False

        for actionTuple in actionTuples:
            bonusSoldiersActionList, attackActionList = actionTuple[0], actionTuple[1]

            self.actionManager.applyListOfActions(bonusSoldiersActionList)

            for attackAction in attackActionList:

                self.actionManager.applyAction(attackAction)
                childTuple = self.maximize(curDepth + 1, maxDepth, game, alpha, beta)  #
                self.actionManager.rollBackAction()

                if (childTuple[0], random()) < (minTuple[0], random()):  #
                    minTuple = (childTuple[0], bonusSoldiersActionList, attackAction)  #

                beta = min(beta, minTuple[0])  #

                if alpha >= beta:
                    broke = True
                    break

            self.actionManager.rollBackNAction(len(bonusSoldiersActionList))

            if broke:
                return minTuple

        return minTuple  #

    def terminalState(self, curDepth: int, maxDepth: int, game: Game) -> bool:
        """
        :param curDepth: current state depth
        :param maxDepth: maximum allowed state depth
        :param game:
        :return: true if the current state is terminal state, false otherwise
        """
        if (curDepth == maxDepth or game.isFinished()):
            self.cnt += 1
            return True
        return False

    def evaluate1(self, game: Game):
        return 3 * game.cityCount[self.isRedPlayer] + game.soldiersCount[
            self.isRedPlayer] * 2

    def evaluate2(self, game: Game):
        return 2 * game.cityCount[self.isRedPlayer] + game.soldiersCount[
            self.isRedPlayer] + 3 * self.heuristicManager.mySecuredCities(self.isRedPlayer, game)

    def evaluate3(self, game: Game):
        return 1 if (game.cityCount[not self.isRedPlayer] == 0) else 0
