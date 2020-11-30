#send game state and return the new game state
#togggle the redArmy boolean in each agent or state
class AggressiveAgent:
    def __init__(self):
        self.cityList = []

    def calculateBonusArmy(self):
        return max(3, len(self.cityList)/3)

    def calculateMaximumCity(self):
        max = 0
        for city in self.cityList:
            if(city.armyCount > max):
                max = city.armyCount
                maxCity = city

        return maxCity

    def AggressiveAgentHeuristic(self):
        bonusArmy = self.calculateBonusArmy()
        maxCity = self.calculateMaximumCity()
        print("bonus army is")
        print(bonusArmy)
        print("Maximum City before adding bonus army")
        print(maxCity)
        #add the bonusArmy to the maxCity in the game state and return it
        maxCity.armyCount+=bonusArmy
        print("Maximum City after adding bonus army")
        print(maxCity)