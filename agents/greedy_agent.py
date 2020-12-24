#send game state and return the new game state
#togggle the redArmy boolean in each agent or state
#check if the parameters are sent by reference not by value
import copy
import math
from queue import PriorityQueue

import game
from game import Game
from agent import Agent
import random

from agent import Agent
from game import Game
#1.place bonus army in the city and check all its adjacents and heuristic is the difference between both armies(myCity and enemyCity)
class GreedyAgent(Agent):
    def __init__(self, isRedArmy):
        self.game = Game
        self.isRed = isRedArmy

    def GreedyHeurictic(self, cityA, cityB, game): #armies in the conquered city - neighbour cities who can conquer me
        #attack from cityA to cityB
        army = cityA.armyCount-1
        cityList = game.cityList
        for neghbourcity in cityB.adjacentcities:
            neighbour = cityList[neghbourcity]
            if neighbour.isRedArmy != self.isRed and neighbour.armyCount > army:
                army-=1
        for neghbourcity in cityA.adjacentcities: #adding this made greedy slower but more safe
            neighbour = cityList[neghbourcity]
            if neighbour.isRedArmy != self.isRed and neighbour.armyCount > army:
                army-=1
        #if army > 0:
        return army
        #return 0;
    def applyHeuristic(self, game: Game):
        q = PriorityQueue()
        bonusSoldiers = game.bonusSoldiers(self.isRed)
        cityListId = game.citiesOf(self.isRed)
        game = self.bonusArmyPlacing(bonusSoldiers, game, self.isRed)
        randomId = random.choice(cityListId)
        canAttack = False
        for cityId in cityListId:
            for neighbourId in game.map.graph[cityId]:
                neighbour = game.cityList[neighbourId]
                city = game.cityList[cityId]
                if (city.armyCount > neighbour.armyCount + 1 and city.isRedArmy != neighbour.isRedArmy):
                    canAttack = True
                    q.put((self.GreedyHeurictic(city, neighbour, game), city, neighbour))
        if (canAttack == False):
                return game
        if (q.not_empty):
            next_item = q.get()
            fromCity = next_item[1]
            toCity = next_item[2]
            print(fromCity)
            print(toCity)
            self.attack(fromCity.id, toCity.id, fromCity.armyCount - 1, game)
        return game


    def attack(self,fromCityId,toCityId,fromCityArmyCount,game):
        game.move(fromCityId,toCityId,fromCityArmyCount)
    # def GreedyMode(self):
    #     bonusArmy = self.calculateBonusArmy()
    #     newCityList = copy.deepcopy(self.game.cityList) #copy by value
    #
    #     GreedyList = []
    #     for city in newCityList:
    #         if city.isRedArmy and self.color == (255,0,0):
    #             newCityList[city.id].armyCount+=bonusArmy
    #             #adjcity is the id of the cities only not the city itself
    #             for adjcity in city.adjacentcities:
    #                 # print(adjcity,  "   adjcity")
    #                 if newCityList[adjcity].isRedArmy is False and newCityList[city.id].armyCount-1 > newCityList[adjcity].armyCount:
    #                     CityListState = copy.deepcopy(newCityList) #deepcopy iterates on objects in the original copy and copies it here
    #                     Heuristic = self.GreedyHeurictic(city,CityListState[adjcity])
    #                     # print(Heuristic , " Heuristic BEfore")
    #                     # print(city, " city")
    #                     # print(CityListState[adjcity], " adjcity")
    #                     attackingArmy = CityListState[city.id].armyCount-1
    #                     CityListState[city.id].armyCount = 1
    #                     CityListState[adjcity].armyCount = attackingArmy
    #                     CityListState[adjcity].isRedArmy = True
    #                     GreedyList.append(tuple([Heuristic,CityListState]))
    #                     # print(CityListState[city.id], " city")
    #                     # print(CityListState[adjcity], " adjcity")
    #             #newCityList[city.id].armyCount-=bonusArmy
    #     maxHeuristic = 0
    #     for i in range (0, len(GreedyList),1):
    #         if GreedyList[i][0] > maxHeuristic:
    #             maxHeuristic = GreedyList[i][0]
    #             state = GreedyList[i][1]
    #             print("max Heuristic " , maxHeuristic)
    #     self.game.cityList = state
    #     print("state after move  ")
    #     for city in self.game.cityList:
    #         print(city)
#need to change the gamestate (citylist in game variable)