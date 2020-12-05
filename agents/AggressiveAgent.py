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

    def attack(self):
        ##shoof elcities ely momken tehgem 3aleha w ehgem 3ala aktar wa7da 3andaha armies
        maxarmy = 0
        for city in self.game.cityList:
            if city.isRedArmy and self.color == (255,0,0):
                for adjcity in city.adjacentcities:
                    if self.game.cityList[adjcity].armyCount < city.armyCount-1 and self.game.cityList[adjcity].armyCount > maxarmy:
                        maxarmy = self.game.cityList[adjcity].armyCount
                        enemycity = self.game.cityList[adjcity]
                        attackingcity = city
        print("maxarmy " , maxarmy)
        print("enemycity " , enemycity)
        print("attackingcity " , attackingcity)
        movingarmy = attackingcity.armyCount-1
        self.game.cityList[attackingcity.id].armyCount-=movingarmy
        self.game.cityList[enemycity.id].armyCount = movingarmy
        self.game.cityList[enemycity.id].redArmy = True
        print("After Attack ")
        print("movingarmy ", movingarmy)
        print("enemycity ", enemycity)
        print("attackingcity ", attackingcity)

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
        self.attack()
