#send game state and return the new game state
#togggle the redArmy boolean in each agent or state
#check if the parameters are sent by reference not by value
import math


class AggressiveAgent:
    def __init__(self, gamestate, color):
        self.game = gamestate
        self.color = color

    def calculateBonusArmy(self):
        list = 0
        if self.color == (255,0,0):
            for city in self.game.cityList:
                if city.isRedArmy == True:
                    list+=1
        else:
            for city in self.game.cityList:
                if city.isRedArmy == False:
                    list+=1
        return math.floor(max(3, list/3))

    def calculateMaximumCity(self):
        max = 0
        for city in self.game.cityList:
            if self.color == (255,0,0):
                if city.armyCount > max and city.isRedArmy == True:
                    max = city.armyCount
                    maxCity = city
            else:
               if city.armyCount > max and city.isRedArmy == False:
                    max = city.armyCount
                    maxCity = city
        return maxCity.id

    def attack(self,maxCity):
        min = self.game.cityList[maxCity].armyCount
        #adjacentcities is a list of ids, city is an  id
        for city in self.game.cityList[maxCity].adjacentcities:
            #fadel condition elcolors yeb2a dynamic
            if self.game.cityList[city].armyCount < min:
                min = self.game.cityList[city].armyCount
                minCity = city
        attackarmy = self.game.cityList[maxCity].armyCount-1
        self.game.cityList[maxCity].armyCount-=attackarmy
        self.game.cityList[minCity].isRedArmy = True
        self.game.cityList[minCity].armyCount +=attackarmy
        print("attacked city  ", minCity, " with army ", attackarmy, "from City ",maxCity)

    def AggressiveAgentHeuristic(self):
        bonusArmy = self.calculateBonusArmy()
        maxCity = self.calculateMaximumCity()
        print(maxCity)
        print("bonus army is")
        print(bonusArmy)
        print("Maximum City before adding bonus army  ", maxCity)
        print(self.game.cityList[maxCity].armyCount)
        #add the bonusArmy to the maxCity in the game state and return it
        self.game.cityList[maxCity].armyCount+=bonusArmy
        print(self.game.cityList[maxCity].armyCount)
        print("Maximum City after adding bonus army")
        print(self.game.cityList[maxCity].armyCount,  "   armycount after")
        self.attack(maxCity)
