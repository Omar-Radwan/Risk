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
        value, bonusArmyActionList, attackAction = self.maximize(0, 2, game, int(-1e9), int(1e9))
        print(f'terimal_states={self.cnt} bonusArmyActionListSize={len(bonusArmyActionList)} value={value}')
        print(f'bonusArmyActionList= {bonusArmyActionList}, bonusSoldiers={game.bonusSoldiers(self.isRedPlayer)}')
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

        actionTuples = self.actionManager.adjacentActions2(self.isRedPlayer)  #
        maxTuple = (int(-1e18), None, None)  #
        broke = False

        for actionTuple in actionTuples:

            bonusSoldiersActionList, attackActionList = actionTuple[0], actionTuple[1]

            self.actionManager.applyListOfActions(bonusSoldiersActionList)

            for attackAction in attackActionList:
                self.actionManager.applyAction(attackAction)
                childTuple = self.minimize(curDepth + 1, maxDepth, game, alpha, beta)  #
                self.actionManager.rollBackAction()

                if childTuple[0] > maxTuple[0]:  #
                    maxTuple = (childTuple[0], bonusSoldiersActionList, attackAction)  #

                alpha = max(alpha, maxTuple[0])  #

                if (alpha >= beta):
                    broke = True
                    break

            self.actionManager.rollBackNAction(len(bonusSoldiersActionList))

            if broke:
                break
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

                if childTuple[0] < minTuple[0]:  #
                    minTuple = (childTuple[0], bonusSoldiersActionList, attackAction)  #

                beta = min(beta, minTuple[0])  #

                if (alpha >= beta):
                    broke = True
                    break

            self.actionManager.rollBackNAction(len(bonusSoldiersActionList))

            if broke:
                break

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
        return (game.cityCount[self.isRedPlayer] * 2 + game.soldiersCount[self.isRedPlayer] -
                game.cityCount[not self.isRedPlayer] * 2 - game.soldiersCount[not self.isRedPlayer])

    def evaluate2(self, game: Game):
        return self.heuristicManager.defensiveAndAttacking(self.isRedPlayer, game)

    def evaluate3(self, game: Game):
        return 1 if (game.cityCount[not self.isRedPlayer] == 0) else 0
