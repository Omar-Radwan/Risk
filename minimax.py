import copy

from Agent import Agent
from Game import Game


class MiniMaxAgent(Agent):
    def applyHeuristic(self, game, bonusPlayers):
        pass

    def start_Traversal(self, game: Game, bonusPlayers: int):
        pass

    def maximize(self):
        pass

    def minimize(self):
        pass

    # *
    # evaluate game state according to numberOfArmy+numberOfCities*2
    # *#
    def evaluate(self, agent: Agent) -> int:
        return agent.countArmy()

    def adjacentStates(self, game: Game, bonusPlayers: int, agent: Agent) -> []:
        result = []
        for i in (0, bonusPlayers + 1):  # max number  = 60/3 -> 20
            maxi = (-1e9, None)
            for c in agent.cityList:  # max number = 60
                # create new copy of game state in which i soldiers are placed at city c
                curGameState = copy.deepcopy(game)
                curGameState.addSoldiersTo(c, i)
                # try to do all moves and find the maximum evaluation
                pass

    def adjacentMoves(self, game: Game, bonusPlayers: int, agent: Agent) -> ():
        for u in agent.cityList:  # max number = 60
            for v in game.map.graph[u]:  # max number = 4
                if (game.cityList[v].isRedArmy != game.cityList[v].isRedArmy and
                        game.cityList[u] - 2 >= game.cityList[v]):  # two cities have different type of armies
                    curGame = copy.deepcopy(game)
                    curGame.move(u, v, curGame.cityList[
                        v] + 1)  # conquer v from u with number of soldiers that can defeat soldiers in v

