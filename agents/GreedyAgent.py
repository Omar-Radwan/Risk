#send game state and return the new game state
#togggle the redArmy boolean in each agent or state
#check if the parameters are sent by reference not by value
import copy
import math

#1.place bonus army in the city and check all its adjacents and heuristic is the difference between both armies(myCity and enemyCity)
class GreedyAgent:
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

    def GreedyHeurictic(self, cityA, cityB):
        return math.fabs(cityA.armyCount - cityB.armyCount)

    def GreedyMode(self):
        bonusArmy = self.calculateBonusArmy()
        newCityList = copy.deepcopy(self.game.cityList) #copy by value

        GreedyList = []
        for city in newCityList:
            if city.isRedArmy and self.color == (255,0,0):
                newCityList[city.id].armyCount+=bonusArmy
                #adjcity is the id of the cities only not the city itself
                for adjcity in city.adjacentcities:
                    # print(adjcity,  "   adjcity")
                    if newCityList[adjcity].isRedArmy is False and newCityList[city.id].armyCount-1 > newCityList[adjcity].armyCount:
                        CityListState = copy.deepcopy(newCityList) #deepcopy iterates on objects in the original copy and copies it here
                        Heuristic = self.GreedyHeurictic(city,CityListState[adjcity])
                        # print(Heuristic , " Heuristic BEfore")
                        # print(city, " city")
                        # print(CityListState[adjcity], " adjcity")
                        attackingArmy = CityListState[city.id].armyCount-1
                        CityListState[city.id].armyCount = 1
                        CityListState[adjcity].armyCount = attackingArmy
                        CityListState[adjcity].isRedArmy = True
                        GreedyList.append(tuple([Heuristic,CityListState]))
                        # print(CityListState[city.id], " city")
                        # print(CityListState[adjcity], " adjcity")
                #newCityList[city.id].armyCount-=bonusArmy
        maxHeuristic = 0
        for i in range (0, len(GreedyList),1):
            if GreedyList[i][0] > maxHeuristic:
                maxHeuristic = GreedyList[i][0]
                state = GreedyList[i][1]
                print("max Heuristic " , maxHeuristic)
        self.game.cityList = state
        print("state after move  ")
        for city in self.game.cityList:
            print(city)
#need to change the gamestate (citylist in game variable)