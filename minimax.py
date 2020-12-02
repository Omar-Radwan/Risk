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
        for i in (0, bonusPlayers + 1):  # max = 17
            maxi = (-1e9, None)
            for c in agent.cityList:  # max number = 50
                # create new copy of game state in which i soldiers are placed at city c
                curGameState = copy.deepcopy(game)
                curGameState.addSoldiersTo(c, i)
                # try to do all moves and find the maximum evaluation
                pass

    def adjacentMoves(self, game: Game, agent: Agent) -> ():
        for u in agent.cityList:  # max number = 50
            for v in game.map.graph[u]:  # max number = 5
                q, r = game.cityList[u], game.cityList[v]
                if (r.isRedArmy != r.isRedArmy and
                        q.armyCount - 2 >= r.armyCount):  # two cities have different type of armies
                    curGame = copy.deepcopy(game)  # a lot of work
                    for i in (r.armyCount + 1, q.armyCount):  # conquer v with v.armyCount+1 .... u.armyCount-1
                        pass

# *
# actions done in each turn:
# place number of soldiers in a city <= 20
# choose a city to conquer from all your cities <=30
# choose number of soldiers to conquer that city with <= *#

# *
# soldiers
# cities
# safe cities except if he adds x soldier
# cities can be attacked
# *#
