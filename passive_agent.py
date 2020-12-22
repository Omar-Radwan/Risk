from agent import Agent
from city import City
from game import Game

class PassiveAgent(Agent):


    def calculateBonusArmy(self,list):
        return max(3,len(list)/3)


    def calculateMinimumTerritory(self,list,game):
        minimum=1e18
        for cityId in list:
            city=game.cityList[cityId]
            if(city.armyCount<minimum):
                minimum=city.armyCount
                minimumTerritory=city

        return minimumTerritory

    def applyHeuristic(self,game:Game)-> Game:
        cityListId=game.citiesOf(True)
        bonusArmy=self.calculateBonusArmy(cityListId)
        minimumTerritory=self.calculateMinimumTerritory(cityListId,game)
        print("bonus army is")
        print(bonusArmy)
        print("minimum territory before adding bonus army")
        print(minimumTerritory)
        minimumTerritory.armyCount+=bonusArmy
        print("minimum territory after adding bonus army")
        print(minimumTerritory)
        game.addSoldiersToCity(minimumTerritory.id,bonusArmy)
        return game

    #def debug(self):
     #   print("bonus for passive Agent is")
      #  print(self.calculateBonus())