from time import sleep

from agent import Agent
from city import City
from game import Game


class HumanAgent(Agent):

    def compareCity(self, x: City, y: City) -> bool:
        """
            given two cities x and y the function returns true if number of soldiers in x is less than number of soldiers in y
            if both cities have the same number of soldiers the function true if id of x is less than id of y
        """
        return x.armyCount < y.armyCount if x.armyCount != y.armyCount else x.id < y.id

    def placeBonusArmy(self, army, city):
        Game.placeBonusSoldiers(city.id, army)

    def applyHeuristic(self, game: Game) -> Game:
        print("human agent move")
       # sleep(0.5)
        return game
