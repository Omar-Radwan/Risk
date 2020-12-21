class PassiveAgent:
    def __init__(self):
        self.cityList = []

    def calculateBonusArmy(self):
        return max(3,len(self.cityList)/3)


    def calculateMinimumTerritory(self):
        minimum=20
        for city in self.cityList:
            if(city.armyCount<minimum):
                minimum=city.armyCount
                minimumTerritory=city

        return minimumTerritory

    def applyHeuristic(self):
        bonusArmy=self.calculateBonusArmy()
        minimumTerritory=self.calculateMinimumTerritory()
        print("bonus army is")
        print(bonusArmy)
        print("minimum territory before adding bonus army")
        print(minimumTerritory)
        minimumTerritory.armyCount+=bonusArmy
        print("minimum territory after adding bonus army")
        print(minimumTerritory)

    #def debug(self):
     #   print("bonus for passive Agent is")
      #  print(self.calculateBonus())