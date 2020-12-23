from agent import Agent
from city import City
from game import Game


class PassiveAgent(Agent):

    def calculateMinimumTerritory(self, list, game):
        minimum = 1e18
        if len(list) != 0:
            minimumTerritory = game.cityList[list[0]]
        else:
            return
        for cityId in list:
            city = game.cityList[cityId]
            if (city.armyCount < minimum):
                minimum = city.armyCount
                minimumTerritory = city

        return minimumTerritory

    def applyHeuristic(self, game: Game) -> Game:
        cityListId = game.citiesOf(self.isRedPlayer)
        bonusArmy = game.bonusSoldiers(self.isRedPlayer)
        minimumTerritor = self.calculateMinimumTerritory(cityListId, game)
        if minimumTerritor != None:
            game.addSoldiersToCity(minimumTerritor.id, bonusArmy)
        return game

    # def debug(self):
    #   print("bonus for passive Agent is")
    #  print(self.calculateBonus())
