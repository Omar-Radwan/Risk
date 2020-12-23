
from queue import PriorityQueue
from game import Game
from agent import Agent

class AStarAgent(Agent):
    def __init__(self):
        pass


    #How many enemy cities can attack me in my new city if I decided to attack this new city.
    def dangerOnDefeatedCityHeuristic(self, enemyCity, newArmyInEnemyCity, danger,game:Game):
            for neighbourId in game.map.graph[enemyCity.id]:
                neighbour=game.cityList[neighbourId]
                if neighbour.isRedArmy==enemyCity.isRedArmy and neighbour.armyCount>newArmyInEnemyCity+1:
                    danger+=2
            return danger

    #How many enemies can attack me in my original city if I left it with only 1 army.
    def dangerOnOriginalCityHeuristic(self, myCity, newArmyInEnemyCity, danger,game:Game):
            for neighbourId in game.map.graph[myCity.id]:
                neighbour=game.cityList[neighbourId]
                if neighbour.isRedArmy!=myCity.isRedArmy and neighbour.armyCount>newArmyInEnemyCity+1:
                    danger+=1
            return danger

    def applyHeuristic(self,game:Game):
        q = PriorityQueue()
        for cityId in game.citiesOf(self.isRedPlayer):
            for neighbourId in game.map.graph[cityId]:
                neighbour=game.cityList[neighbourId]
                city=game.cityList[cityId]
                if(city.armyCount>neighbour.armyCount+1 and city.isRedArmy!=neighbour.isRedArmy):
                    print("city id : ",city.id," with ",city.armyCount," armies",
                          " and red color is ",city.isRedArmy,"can attack ","neighbour id : ",
                          neighbour.id," with armies ",neighbour.armyCount," armies"," and red color is : ",
                          neighbour.isRedArmy)
                    # heuristic 1
                    numberOfDefeatedEnemies=neighbour.armyCount
                    # heuristic 2
                    dangerOnDefeatedCity=self.dangerOnDefeatedCityHeuristic(neighbour,city.armyCount-1,0,game)
                    # heuristic 3
                    dangerOnOriginalCity=self.dangerOnOriginalCityHeuristic(city,1,0,game)
                    totalHeuristic=numberOfDefeatedEnemies-dangerOnDefeatedCity-dangerOnOriginalCity
                    q.put((totalHeuristic*-1,city,neighbour))
                    #print("total heu ",totalHeuristic)

        if (q.not_empty):
            next_item = q.get() #a7la action
            fromCity=next_item[1] #a7la from city
            toCity=next_item[2] # a7la to city
            print(fromCity)
            print(toCity.id)
            print(fromCity.armyCount-1)
            self.attack(fromCity.id,toCity.id,fromCity.armyCount-1,game)
            return game

    def attack(self,fromCityId,toCityId,fromCityArmyCount,game):
        game.move(fromCityId,toCityId,fromCityArmyCount)